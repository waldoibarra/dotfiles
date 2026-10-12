// Check installed Pi delegation; --live MODEL_A MODEL_B explicitly enables inference.
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir, tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { pathToFileURL } from "node:url";

const live = process.argv[2] === "--live";
assert(process.argv.length === (live ? 5 : 2), "Usage: node check-pi-harness.mjs [--live A B]");
const selectedModels = process.argv.slice(3);
if (live) {
  assert(selectedModels.every(model => model.includes("/")), "Use exact provider/model IDs");
  assert.notEqual(selectedModels[0], selectedModels[1], "Use two distinct models");
}
const executable = realpathSync(execFileSync("which", ["pi"], { encoding: "utf8" }).trim());
const searchRoots = createRequire(executable).resolve.paths("@earendil-works/pi-coding-agent");
const candidates = [dirname(dirname(executable)),
  ...searchRoots.map(root => join(root, "@earendil-works/pi-coding-agent"))];
const hostRoot = realpathSync(process.env.PI_PACKAGE_DIR ?? candidates.find(candidate => {
  const manifest = join(candidate, "package.json");
  return existsSync(manifest) &&
    JSON.parse(readFileSync(manifest, "utf8")).name === "@earendil-works/pi-coding-agent";
}));
process.env.PI_OFFLINE = "1";
process.env.PI_SUBAGENTS_PI_CODING_AGENT_PACKAGE_ROOT = hostRoot;
const { createAgentSession, DefaultResourceLoader, SettingsManager, SessionManager } =
  await import(pathToFileURL(join(hostRoot, "dist/index.js")));
const cwd = mkdtempSync(join(tmpdir(), "dotfiles-pi-harness-"));
const agentDir = join(homedir(), ".pi/agent");
const runner = join(agentDir, "npm/node_modules/pi-subagents/index.js");
assert(existsSync(runner), "Install the configured pi-subagents pin before checking");
writeFileSync(join(cwd, "AGENTS.md"), "# Fixture\n\nFixture marker: shared-role-fixture.\n");
const settingsManager = SettingsManager.create(cwd, agentDir, { projectTrusted: false });
let context;
const resourceLoader = new DefaultResourceLoader({
  cwd, agentDir, settingsManager, noExtensions: true,
  additionalExtensionPaths: [runner],
  extensionFactories: [pi => {
    pi.on("session_start", (_event, ctx) => { context = ctx; });
  }],
});
await resourceLoader.reload();
assert.deepEqual(resourceLoader.getExtensions().errors, []);
const { session } = await createAgentSession({
  cwd, agentDir, settingsManager, resourceLoader,
  sessionManager: SessionManager.create(cwd, join(cwd, "sessions")),
});
const expectedRoles = [
  "browser-tester", "code-auditor", "docs-writer", "implementer", "plan-reviewer",
];
const task = "Configuration smoke check only. Do not call tools, delegate, or change files. " +
  "Reply with the fixture marker from project instructions and your role heading.";
let sequence = 0;
async function call(name, params) {
  const tool = session.getToolDefinition(name);
  assert(tool, `Missing tool: ${name}`);
  return tool.execute(`check-${++sequence}`, params, undefined, undefined, context);
}
function save(name, result) {
  writeFileSync(join(cwd, `${name}.json`), JSON.stringify(result, null, 2));
}
function checkChild(child, role, model) {
  assert.equal(child.exitCode, 0, JSON.stringify(child));
  assert.equal(child.agent, role);
  const records = readFileSync(child.sessionFile, "utf8").trim().split("\n").map(JSON.parse);
  const system = records.filter(record => record.message?.role === "system");
  const prompt = JSON.stringify(system);
  for (const marker of ["# Global instructions", "shared-role-fixture", "shell-scripting",
    readFileSync(join(homedir(), ".agents/roles", `${role}.md`), "utf8")
      .split("---", 3)[2].trim()]) {
    // JSON encoding escapes newlines; compare strings in their serialized form.
    assert(prompt.includes(JSON.stringify(marker).slice(1, -1)),
      `Missing child context: ${marker}`);
  }
  const slash = model.indexOf("/");
  const provider = model.slice(0, slash);
  const id = model.slice(slash + 1).replace(/:(off|minimal|low|medium|high|xhigh|max)$/, "");
  const replies = records.filter(record => record.message?.role === "assistant");
  assert(replies.length > 0, "No provider response");
  for (const { message } of replies) {
    assert.equal(message.provider, provider);
    assert.equal(message.model, id);
    assert.notEqual(message.stopReason, "error");
  }
}
try {
  await session.bindExtensions({ mode: "print", onError: error => { throw error; } });
  const catalog = await call("subagent", {
    action: "list", options: { agentScope: "user", capabilities: true },
  });
  save("catalog", catalog);
  assert.deepEqual(catalog.details.agentCapabilities.agents.map(agent => agent.name).sort(),
    expectedRoles);
  for (const params of [
    { agent: "missing-fixture-role", task },
    { agent: "plan-reviewer", model: "missing-fixture-provider/missing-fixture-model", task },
  ]) {
    await assert.rejects(() => call("subagent", { ...params, async: false }),
      params.model ? /missing-fixture-provider\/missing-fixture-model/ : /Unknown agent/);
  }
  for (const params of [
    { model: "openai-codex/gpt-6-astra:low" },
    ...(session.model?.id.includes("astra") ? [{}] : []),
  ]) {
    await assert.rejects(() => call("subagent", {
      agent: "code-auditor", ...params, task, async: false,
    }), /outside the configured subagent model scope/);
  }
  assert.equal(session.steeringMode, "all");
  console.log("PASS: role discovery, leader rejection, and all-message steering configuration");
  if (live) {
    const foreground = [
      ["plan-reviewer", selectedModels[0]], ["code-auditor", selectedModels[1]],
      ["docs-writer", selectedModels[0]],
    ];
    for (const [agent, model] of foreground) {
      const result = await call("subagent", {
        agent, model, task, async: false,
        options: { agentScope: "user", timeoutMs: 120000 },
      });
      save(agent, result);
      assert(!result.isError, JSON.stringify(result));
      checkChild(result.details.results[0], agent, model);
    }
    // Separate background launches allow different models without scripted workflows.
    const receipts = await Promise.all(["implementer", "browser-tester"].map((agent, index) =>
      call("subagent", {
        agent, model: selectedModels[index], task, async: true,
        options: { agentScope: "user", timeoutMs: 120000 },
      })));
    for (const [index, receipt] of receipts.entries()) {
      assert(!receipt.isError, JSON.stringify(receipt));
      const id = receipt.details.runId;
      await call("bg_wait", { id, timeoutMs: 150000, stopOnAttention: false });
      const statusFile = join(receipt.details.asyncDir, "status.json");
      const status = JSON.parse(readFileSync(statusFile, "utf8"));
      save(`background-${index}`, status);
      assert.equal(status.state, "complete");
      assert.equal(status.processTerminal.state, "observed");
      checkChild(status.steps[0], ["implementer", "browser-tester"][index], selectedModels[index]);
    }
    console.log("PASS: roles, explicit worker models, context, mixed-model background runs");
  }
  console.log(`Private runtime evidence: ${cwd}`);
} finally {
  session.dispose();
}
