"""Coordinate Brew and Mise updates without replacing Mise while it is running."""

import os
from pathlib import Path
import signal
import subprocess
import sys
import threading


class Runner:
  """Own subprocess groups so interruption cannot leave package updates running."""

  def __init__(self):
    self.children = []
    self.readers = []
    self.output_lock = threading.Lock()
    self.output_errors = []

  def relay(self, child, label):
    """Drain each merged stream concurrently, including carriage-return progress updates."""
    try:
      with child.stdout:
        for line in child.stdout:
          message = line.rstrip("\n")
          with self.output_lock:
            print(f"[{label}] {message}", flush=True)
    except OSError as error:
      self.output_errors.append(error)

  def start(self, command, env=None, label=None, **kwargs):
    if label:
      kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                    encoding="utf-8", errors="replace")
    child = subprocess.Popen(command, env=env, start_new_session=True, **kwargs)
    self.children.append(child)
    if label:
      with self.output_lock:
        print(f"[{label}] Starting updates.", flush=True)
      reader = threading.Thread(target=self.relay, args=(child, label), daemon=True)
      self.readers.append(reader)
      reader.start()
    return child

  def finish_output(self):
    for reader in self.readers:
      reader.join()
    if self.output_errors:
      raise self.output_errors[0]

  def run(self, command, **kwargs):
    child = self.start(command, **kwargs)
    code = child.wait()
    if code:
      raise subprocess.CalledProcessError(code, command)

  def stop(self):
    # Completed commands no longer own a PID; avoid signaling a reused process ID.
    active = [child for child in self.children if child.poll() is None]
    for child in active:
      try:
        os.killpg(child.pid, signal.SIGTERM)
      except ProcessLookupError:
        pass
    for child in active:
      try:
        child.wait(timeout=5)
      except subprocess.TimeoutExpired:
        pass
      try:
        os.killpg(child.pid, signal.SIGKILL)
      except ProcessLookupError:
        pass
      child.wait()
    for reader in self.readers:
      reader.join(timeout=5)


def interrupt(signum, _frame):
  raise SystemExit(128 + signum)


def main():
  runner = Runner()
  signal.signal(signal.SIGTERM, interrupt)
  signal.signal(signal.SIGINT, interrupt)
  try:
    probe = runner.start(
      ["brew", "list", "--formula", "--versions"], stdout=subprocess.PIPE, text=True
    )
    installed, _ = probe.communicate()
    if probe.returncode:
      raise subprocess.CalledProcessError(probe.returncode, probe.args)
    has_mise = any(line.split()[0] == "mise" for line in installed.splitlines() if line)
    if os.environ.get("DOTS_SEQUENTIAL") == "1" or not has_mise:
      print("Syncing Brew and Mise sequentially.", flush=True)
      runner.run(["just", "brew"])
      runner.run(["just", "mise-sync"])
      return

    # Refresh the Brew-owned executable before either update lane starts.
    print("Updating the Mise executable before parallel tool updates.", flush=True)
    runner.run(["brew", "upgrade", "mise"])
    prefix = runner.start(
      ["brew", "--prefix", "mise"], stdout=subprocess.PIPE, text=True
    )
    directory, _ = prefix.communicate()
    if prefix.returncode:
      raise subprocess.CalledProcessError(prefix.returncode, prefix.args)
    mise_bin = str(Path(directory.strip()) / "bin")
    runner.run([str(Path(mise_bin) / "mise"), "--version"])
    brew_env = dict(os.environ)
    skips = brew_env.get("HOMEBREW_BUNDLE_BREW_SKIP", "").split()
    brew_env["HOMEBREW_BUNDLE_BREW_SKIP"] = " ".join(dict.fromkeys([*skips, "mise"]))
    mise_env = dict(os.environ, PATH=mise_bin + os.pathsep + os.environ["PATH"])
    print("Syncing Brew and Mise in parallel; cleanup waits for both.", flush=True)
    brew = runner.start(["just", "brew-apply"], env=brew_env, label="brew")
    mise = runner.start(["just", "mise-sync"], env=mise_env, label="mise")
    # Reap both lanes even if one fails; never clean up after a failed update.
    codes = [brew.wait(), mise.wait()]
    runner.finish_output()
    for child, code in zip((brew, mise), codes):
      if code:
        raise subprocess.CalledProcessError(code, child.args)
    runner.run(["just", "brew-clean"])
  finally:
    runner.stop()


if __name__ == "__main__":
  try:
    main()
  except (OSError, subprocess.CalledProcessError) as error:
    print(f"Package sync failed: {error}", file=sys.stderr)
    sys.exit(1)
