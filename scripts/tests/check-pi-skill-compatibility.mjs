// Verify Dotbot delivery and native Pi prompt loading without inference.
import assert from "node:assert/strict";
import {
  lstatSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

assert(process.env.PI_PACKAGE_DIR, "Set PI_PACKAGE_DIR to the installed coding-agent package root");
const hostRoot = realpathSync(process.env.PI_PACKAGE_DIR);
const root = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const home = mkdtempSync(join(tmpdir(), "dotfiles-pi-skills-"));
const source = join(root, "home/.pi/agent/APPEND_SYSTEM.md");
const expected = readFileSync(source, "utf8").trim();
const shared = join(root, "home/.agents/AGENTS.md");
const sharedBytes = readFileSync(shared, "utf8");
const originalHome = process.env.HOME;
let session;

try {
  process.env.HOME = home;
  process.env.PI_OFFLINE = "1";
  const agentDir = join(home, ".pi/agent");
  const installed = join(agentDir, "APPEND_SYSTEM.md");
  let previousMtime;
  for (let run = 0; run < 2; run++) {
    const result = spawnSync("python3", [
      join(root, "dotbot/bin/dotbot"), "-d", root, "-c", join(root, "install.conf.yaml"),
      "--only", "create", "link",
    ], { encoding: "utf8", timeout: 30000 });
    assert.equal(result.status, 0, result.error?.message ?? result.stdout + result.stderr);
    assert(lstatSync(installed).isSymbolicLink());
    assert.equal(realpathSync(installed), source);
    assert.equal(readFileSync(installed, "utf8").trim(), expected);
    const mtime = lstatSync(installed).mtimeMs;
    if (run) assert.equal(mtime, previousMtime, "Repeated delivery preserves the link");
    previousMtime = mtime;
    for (const relative of [".agents/AGENTS.md", ".pi/agent/AGENTS.md", ".claude/CLAUDE.md"]) {
      assert.equal(realpathSync(join(home, relative)), shared);
      assert.equal(readFileSync(join(home, relative), "utf8"), sharedBytes);
    }
  }

  const { createAgentSession, DefaultResourceLoader, SettingsManager, SessionManager } =
    await import(pathToFileURL(join(hostRoot, "dist/index.js")));
  const cwd = join(home, "workspace");
  mkdirSync(join(cwd, ".pi"), { recursive: true });
  const projectMarker = "Project-specific append marker.";
  writeFileSync(join(cwd, ".pi/APPEND_SYSTEM.md"), projectMarker);
  for (const projectTrusted of [false, true]) {
    const settingsManager = SettingsManager.inMemory({}, { projectTrusted });
    const resourceLoader = new DefaultResourceLoader({
      cwd, agentDir, settingsManager,
      noExtensions: true, noSkills: true, noPromptTemplates: true, noThemes: true,
    });
    await resourceLoader.reload();
    ({ session } = await createAgentSession({
      cwd, agentDir, settingsManager, resourceLoader,
      sessionManager: SessionManager.inMemory(cwd), tools: ["read"],
    }));
    assert(session.systemPrompt.includes(sharedBytes.trim()), "Shared policy remains loaded");
    assert.equal(session.systemPrompt.includes(expected), !projectTrusted);
    assert.equal(session.systemPrompt.includes(projectMarker), projectTrusted);
    session.dispose();
    session = undefined;
  }
  console.log("PASS: Pi-only link is idempotent; shared instructions remain unchanged");
  console.log("PASS: Pi loads compatibility instructions; project override replaces them");
  console.log("No inference ran; model compliance remains a separate check");
} finally {
  session?.dispose();
  if (originalHome === undefined) delete process.env.HOME;
  else process.env.HOME = originalHome;
  rmSync(home, { recursive: true, force: true });
}
