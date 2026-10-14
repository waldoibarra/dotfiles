// Verify the selected compiled host's session storage without provider calls.
import assert from "node:assert/strict";
import { existsSync, mkdtempSync, readFileSync, realpathSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

assert(process.env.PI_PACKAGE_DIR, "Set PI_PACKAGE_DIR to the compiled coding-agent package root");
const hostRoot = realpathSync(process.env.PI_PACKAGE_DIR);
const manifest = JSON.parse(readFileSync(join(hostRoot, "package.json"), "utf8"));
assert.equal(manifest.name, "@earendil-works/pi-coding-agent");
const entrypoint = join(hostRoot, "dist/index.js");
assert(existsSync(entrypoint), "Build the selected host first; this fixture never builds it");
process.env.PI_OFFLINE = "1";
const { SessionManager } = await import(pathToFileURL(entrypoint));
const workspace = mkdtempSync(join(tmpdir(), "dotfiles-pi-session-"));
try {
  const sessionDir = join(workspace, "sessions");
  const first = SessionManager.create(workspace, sessionDir);
  const firstFile = first.getSessionFile();
  assert(firstFile, "persistent session should select a session file");
  first.appendMessage({ role: "user", content: "offline persistence fixture" });
  assert(existsSync(firstFile), "first user message should flush the session file");

  const resumed = SessionManager.continueRecent(workspace, sessionDir);
  assert.equal(resumed.getSessionFile(), firstFile, "continueRecent should resume latest session");
  const branch = resumed.getBranch();
  assert.equal(branch.length, 1, "resumed branch should contain the saved user message");
  assert.deepEqual(branch[0].message, { role: "user", content: "offline persistence fixture" });

  const memory = SessionManager.inMemory(workspace);
  memory.appendMessage({ role: "user", content: "unsaved fixture" });
  assert.equal(memory.getSessionFile(), undefined, "in-memory mode must not select a file");
  const version = manifest.version;
  console.log(`PASS: compiled host ${version} persisted and resumed the synthetic session`);
} finally {
  // SessionManager performs synchronous file operations; no process or provider was started.
  rmSync(workspace, { recursive: true, force: true });
}
