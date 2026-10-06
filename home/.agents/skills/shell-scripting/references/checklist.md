# Shell Scripting Checklist

The operational rubric for this skill. Bracketed section names refer to the bundled
[Google Shell Style Guide](google-shell-style-guide.md). **DEVIATION** marks a deliberate
departure from an explicit Google rule; the checklist wins on conflicts.

- **Audit or fix:** walk all ten sections against the requested scripts, reporting correctness
  before portability and style. Do not expand the edit scope to an unrequested migration.
- **Create:** choose the [structured](../assets/template.sh) or
  [linear](../assets/template-linear.sh) Bash template using §8.
- **POSIX `sh`:** apply the target gate in §1 before using any Bash-specific rule or example.

## Contents

1. [Which shell and when](#1-which-shell--when-background)
2. [Files and shebang](#2-files--shebang-shell-files-and-interpreter-invocation)
3. [Strict mode and environment](#3-strict-mode--environment-environment-arithmetic)
4. [Comments](#4-comments-comments)
5. [Formatting](#5-formatting-formatting)
6. [Variable expansion and quoting](#6-variable-expansion--quoting-variable-expansion-quoting)
7. [Features and bugs](#7-features--bugs-features-and-bugs)
8. [Naming and structure](#8-naming--structure-naming-conventions)
9. [Calling commands](#9-calling-commands-calling-commands)
10. [When in doubt](#10-when-in-doubt-when-in-doubt-be-consistent)

---

## 1. Which shell & when [§Background]

- Bash for anything non-trivial; POSIX `sh` only when the target forces it
  (minimal Alpine/BusyBox, constrained boot environments). _Why:_ bashisms
  (`[[ ]]`, arrays, `local`) are worth having when Bash is available.
  For POSIX `sh`, use `[ ]`/`test`, `=` for string equality, `$(( ))` for arithmetic
  expansion, and positional parameters where suitable. Bash arrays, `local`, `[[ ]]`,
  process substitution, `BASH_SOURCE`, and Bash traps are not portable substitutes.
  Check shell/version support for options such as `pipefail`; do not add an unsupported
  option merely to satisfy the Bash default.
- Shell is for **small utilities and wrappers**. Past ~100 lines or with
  non-trivial data structures/control flow, recommend a real language. _Why:_
  shell's error handling and data handling don't scale; it gets unmaintainable.
- **Idempotency (for re-runnable scripts).** If a script is meant to run more than
  once — installers, setup/bootstrap, provisioning, CI — make operations
  check-before-act so a re-run is a safe no-op: `command -v foo >/dev/null ||
  install foo`; `grep -qxF "${line}" "${file}" || echo "${line}" >> "${file}"`.
  _Why:_ re-running is the normal case for setup scripts. Not needed for a one-shot
  script run exactly once.

## 2. Files & shebang [§Shell Files and Interpreter Invocation]

- **DEVIATION:** shebang is `#!/usr/bin/env bash`, not Google's `#!/bin/bash`.
  _Why:_ portability — Bash isn't always at `/bin/bash`; on macOS `/bin/bash` is
  frozen 3.2. Exception: POSIX-only target → `#!/bin/sh`.
- Executables: `.sh` extension or none. **Libraries: `.sh` extension, not
  executable, no shebang.** _Why:_ a sourced file inheriting the caller's shell
  shouldn't declare its own interpreter.
- Never SUID/SGID a shell script. _Why:_ unsecurable; use `sudo` instead.

## 3. Strict mode & environment [§Environment; §Arithmetic]

- Standalone **Bash** executables start with `set -euo pipefail`. _Why:_ expose unset
  variables and pipeline failures. These options do not replace explicit error handling.
  For POSIX `sh`, select supported options and check failures without relying on Bash features.
- **Sourced libraries: no `set`** (and no shebang). _Why:_ they inherit the
  caller's options; overriding them surprises the caller.
- Before enabling strict mode, review the failure paths:
  1. Split declaration from command-substitution assignment (§8).
  2. Use `${VAR:-}` for legitimately optional values; validate required ones instead of
      hiding a missing prerequisite behind an empty default.
  3. Handle expected nonzero statuses explicitly, then enable the supported flags.
      Bare `(( i++ ))` returns nonzero when its value is zero (§7); a no-match `grep`
      also returns nonzero without necessarily indicating an error.
  These steps are a starting review, not a guarantee that a script is “fully guarded.”
  `-e` is suppressed in conditionals and certain `&&`/`||` contexts, including inside
  functions called from those contexts. Command substitutions and process substitutions
  need their own failure analysis; the consuming command's success does not prove a
  process-substitution producer succeeded. See Bash's
  [set builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
  for the exact `errexit` exceptions.
- Errors/warnings → **STDERR**; normal status → **STDOUT**. Use an `err()`
  helper. _Why:_ lets a caller separate real problems from chatter
  (`2>/dev/null`, `2>&1 | grep`). Keep output plain — no decorative emoji; they
  add noise without signal.

  ```bash
  err() { echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2; }
  ```

## 4. Comments [§Comments]

Use file and function headers; add implementation and TODO comments only when applicable.

- **File header** — every file opens with a one-line description of what it does
  (copyright/author optional). _Why:_ the reader knows the script's job before
  reading a line of logic.

  ```bash
  #!/usr/bin/env bash
  #
  # Perform hot backups of Oracle databases.
  ```

- **Function comments — DEVIATION:** every function except `main()` gets a header,
  including obvious or short helpers. Describe the contract using only the relevant sections:
  Description, Globals (used/modified), Arguments, Outputs (STDOUT/STDERR), and Returns
  (statuses beyond the last command's). _Why:_ a caller should not need to read the body.
  This is the skill's house policy, not a claim that an uncommented function is technically
  broken. Flag missing headers during audits even when siblings also lack them; keep any
  migration within the authorized scope (§10).

  ```bash
  #######################################
  # Cleanup files from the backup directory.
  # Globals:
  #   BACKUP_DIR
  # Arguments:
  #   None
  #######################################
  cleanup() { ... }
  ```

- **Implementation comments** — comment only the tricky, non-obvious, or important
  parts; explain the _why_, not the _what_. _Why:_ narrating obvious lines is
  noise that ages badly.
- **TODO comments** — `TODO` in all caps + an identifier (name/bug):
  `# TODO(waldo): handle the unlikely edge case (bug 123)`. _Why:_ greppable, and
  says who has the context.

## 5. Formatting [§Formatting]

- 2-space indent, no tabs (exception: `<<-` heredoc bodies). Match `.editorconfig`
  if present.
- **DEVIATION:** 100-char line default (Google says 80) — or whatever
  `.editorconfig` sets. Long URLs/paths may exceed; factor into a variable or a
  heredoc where it helps.
- Pipelines/`&&`/`||` that don't fit on one line: split one segment per line, the
  operator leading the continuation, 2-space indent. _Why:_ distinguishes a
  pipeline from ordinary line continuation.
- `; then` / `; do` on the same line as `if`/`for`/`while`; `else`/`fi`/`done` on
  their own lines. Include `in "$@"` in for-loops for clarity.
- `case`: alternatives indented 2 spaces; `;;` per the guide's layout.

## 6. Variable expansion & quoting [§Variable expansion; §Quoting]

- **Quote everything** with a variable, command substitution, space, or meta
  char: `"${var}"`, `"$(cmd)"`. _Why:_ unquoted → word-splitting + globbing.
- Prefer `"${var}"` over `"$var"`; don't brace single-char specials (`$1`, `$?`).
- `"$@"` to pass args through, **never** `$*` (except joining into one string).
  _Why:_ `"$@"` preserves argument boundaries; `$*` collapses/splits them.
- Braces are not quoting — you still need the double quotes.

## 7. Features & bugs [§Features and Bugs]

- **ShellCheck is the mechanical floor** — run it, don't re-derive it by hand.
- `$(cmd)` never backticks. _Why:_ nests cleanly, readable.
- `[[ ]]` over `[ ]`/`test`. _Why:_ no word-splitting/glob inside; supports `=~`.
- Test strings with `-z`/`-n` and `==`; use `(( ))` (or `-lt`/`-gt`) for numeric
  comparison. _Why:_ `<`/`>` in `[[ ]]` are lexicographic — a silent bug.
- Wildcards: use `./*` not `*`. _Why:_ a file named `-rf` becomes a flag.
- **Guard glob-based iteration.** An unmatched filename glob remains literal unless
  `nullglob` is enabled, so a `for` loop can run once with a nonexistent path. Use
  `[[ -e "$item" ]] || continue`, include `-L` if dangling symlinks belong in the input,
  or scope `shopt -s nullglob`. A `case` pattern is pattern matching, not filename
  expansion. ShellCheck does not establish whether a runtime glob has matches.
- **Never `eval`.** _Why:_ unpredictable, unauditable.
- Arrays for lists/flag sets: `flags=(--foo --bar); cmd "${flags[@]}"`. _Why:_
  safe quoting; strings-as-lists force `eval`/nested quotes.
- **A piped `while` normally runs in a subshell** in Bash, so its variable changes do
  not survive. Process substitution (`while read -r ...; do ...; done < <(cmd)`) keeps
  the loop in the current shell, but does not propagate the producer's failure through
  the loop's status. Check the producer separately when its success matters. `readarray`
  is another option only on Bash versions that support it.
- Arithmetic: `(( ))` / `$(( ))`, never `let`/`expr`/`$[ ]`. Beware a standalone
  `(( i++ ))` evaluating to 0 → non-zero exit → death under `set -e`.
- No aliases in scripts — use functions.
- **Environment awareness:** check the target's utilities and versions before using
  divergent `sed -i`, `date`, or `readlink` flags. Linux does not imply GNU utilities;
  macOS/BSD does not establish one fixed flag set across releases. Avoid Bash-4+ features
  (`declare -A`, `${var^^}`, `mapfile`) on Bash 3.2. Use the
  [target-environment gate](../SKILL.md#establish-the-target) rather than assuming.

## 8. Naming & structure [§Naming Conventions]

**Meaning comes before case.** A name's first job is to say what the thing is
_for_ — its purpose at the right altitude — not how it's built, and not a generic
placeholder. Check meaning first, then apply the case rules below.

- **Flag and rename vague names.** `content`, `data`, `tmp`, `val`, `result`,
  `x`, `str`, `arr` describe a _type or shape_, not a _role_. Replace with the
  role: the line written into sudoers is a `sudoers_directive`, not `content`;
  a path to the backup is `backup_path`, not `file`. _Why:_ the reader (human
  or model) should understand the variable without tracing where it came from.
- **The name must match the behavior.** If a function is called
  `delete_temp_files` but also uploads them, the name lies — rename the function
  or split it. A name that under- or mis-describes its contents costs more than a
  long, accurate one.
- **Altitude matches scope.** A single-letter loop index (`for i in ...`) is fine;
  a one-letter script-level variable is not. The wider the scope, the more the
  name must carry.
- **File names describe the script's job**, in **kebab-case**.
  `configure-touch-id-for-sudo.sh` tells you exactly what it does; `script.sh`,
  `run.sh`, `utils.sh`, `helper.sh` hide it. **DEVIATION:** Google uses
  `snake_case` and forbids hyphens (`make_template`, not `make-template`); this
  skill enforces **kebab-case** for shell file names instead. If a project's
  existing scripts use a different case, match them (§10).

- Functions: `lower_snake`; `::` for library packages; `()` required; `function`
  keyword optional but consistent within a project.
- Do **not** use a leading underscore to mark private helpers or locals. This skill names
  by role instead; the prefix supplies no enforced Bash privacy. Flag the convention as a
  house-policy finding even if it is consistent, and recommend a separately scoped migration
  rather than silently renaming unrelated code (§10).
- Constants & exported/global vars: `UPPER_SNAKE`, declared at the top as appropriate.
  Use `readonly` for constants and `export` for environment variables.
  Mark constants `readonly` even for literal values or simple expansions; the absence of
  command substitution removes the masking risk, not the constant's immutability contract.
- `local` for every function variable. _Why:_ avoids leaking into the global
  namespace and clobbering something meaningful.
- **Split declaration from command-substitution assignment.** `local`, `local -r`,
  `readonly`, `declare`, and `export` return the declaration's status, usually zero,
  masking the substitution's status.

  ```bash
  local my_var
  my_var="$(cmd)"     # The assignment now exposes cmd's status.
  # local my_var="$(cmd)"   # DON'T: the declaration masks cmd's failure.
  ```

  Assign runtime-computed constants before marking them `readonly`. This exposes a
  substitution's status but does not remove the `set -e` exceptions in §3.
  [SC2155](https://www.shellcheck.net/wiki/SC2155) documents this failure, but default
  checking does not cover every declaration form. For example, `local -r` needs
  `check-extra-masked-returns` for a warning. Inspect all forms rather than treating a
  clean lint result as proof.
- Functions grouped below constants; **no executable code between functions.**
  Only includes, `set`, and constants precede function definitions.
- **Order helper functions bottom-up by call depth.** Read the file from
  `main` (bottom-most, depth 0) upward: directly above `main` sit the functions
  it calls, in the order it calls them (depth 1); above those sit the functions
  _they_ call, in their call order (depth 2); and so on outward. Reading
  bottom-to-top walks the call graph breadth-first, from the entry point out to
  its leaves. _Why:_ gives every function one deterministic slot — no guessing
  between alphabetical, "logical grouping," or first-appearance — and it extends
  `main`'s own bottom-most placement instead of contradicting it with a
  top-down reading for everything else.

  ```text
  get_color_for_bar        # depth 2 — build_bar_section's only callee
  print_status_line        # depth 1 — main's last call
  build_git_section        # depth 1 — main's 6th call
  build_directory_section  # depth 1 — main's 5th call
  build_duration_section   # depth 1 — main's 4th call
  build_cost_section       # depth 1 — main's 3rd call
  build_bar_section        # depth 1 — main's 2nd call; calls get_color_for_bar
  build_model_section      # depth 1 — main's 1st call
  main                     # depth 0
  ```

  **Shared helpers (diamond dependencies) break the call-order tie-break.** The
  example above is a clean tree — one caller per callee. If a function is
  called by more than one other function (e.g. a leaf helper invoked both
  directly by `main` _and_ indirectly through one of `main`'s own callees),
  "which caller's call order?" has no single answer. Fall back to the
  invariant the heuristic exists to approximate: **a callee must sit above
  every one of its callers, full stop.** Place the shared helper at the top of
  its depth group so it clears all callers at once; use call-order only to
  break ties among true siblings that share no callee.

  ```text
  get_os_name              # leaf — called by main AND by set_default_shell
  get_brew_zsh_path        # leaf — called by main AND by set_default_shell
                            #        AND by add_to_allowed_shells
  set_default_shell        # depth 1 — main's last call
  add_to_allowed_shells    # depth 1 — main's first call
  main                     # depth 0
  ```

- **`source` at the top level, not inside a function** — this matches Google's
  "includes before functions," keeps dependencies visible, and avoids wrapping the
  path-resolving `local dir="$(...)"` in the masking bug above. Don't hide `source`
  calls inside a helper function.
- **Introduce a function only when it earns its place:** it's called more than
  once, isolates a genuinely distinct and nameable step, or must be sourced to be
  tested. _Why:_ a function that wraps the whole body and runs exactly once is
  indirection with no payoff. If the only reason to add one is to give `main`
  something to call, don't — keep the script flat: no functions, no `main`, no
  guard. Decide whether you need functions _first_; `main` follows only if you do.
- `main` is required **only when the script defines ≥1 other function**; a short,
  linear script doesn't need one (Google: "for short scripts where it's just a
  linear flow, `main` is overkill and so is not required"). _Why main, when used:_
  obvious entry point; lets everything else be `local`.
- **Guard the Bash `main` call** so sourcing skips the application entry point.
  Top-level `set`, includes, and constants still execute and can change the caller's
  environment. Source such executables in an isolated test shell; reusable sourced libraries
  follow §2–§3 and do not run an entry point. The Bash guard below is not portable POSIX `sh`.

  ```bash
  if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
  fi
  ```

## 9. Calling commands [§Calling Commands]

- Always check return values — `if ! cmd; then err ...; exit 1; fi`, or
  `PIPESTATUS` for a specific stage of a pipe (copy it immediately; `[` clobbers
  it). _Why:_ a command that failed and wasn't checked corrupts later state.
- **Clean up with `trap`.** Register script-owned cleanup with `EXIT` so ordinary exits
  and `set -e` aborts do not skip it: `tmp=$(mktemp); trap 'rm -f "${tmp}"' EXIT`.
  An early function `return` does not exit the shell. For function-owned resources,
  use explicit cleanup or a deliberately scoped Bash `RETURN` trap; preserve existing
  traps and ensure cleanup variables remain available when the trap runs. Traps cannot
  guarantee cleanup after uncatchable termination such as `SIGKILL`. An optional `ERR`
  diagnostic follows the same conditional-execution exceptions as `errexit` (§3).
- Prefer Bash builtins / parameter expansion over spawning `sed`/`awk`/`expr` for
  simple string/number work. _Why:_ faster, more robust, fewer portability traps.

## 10. When in doubt [§When in Doubt: Be Consistent]

- Match the surrounding code on **neutral** choices (indent, case, `function`
  keyword) over any personal preference. Consistency is the tie-breaker when
  there's no technical argument.
- Still report correctness defects such as masked command-substitution status, even if the
  surrounding code repeats them.
- Report the skill's house policies separately: strict mode for standalone Bash executables,
  headers for every function except `main`, and no leading-underscore private markers.
  Consistency does not waive this rubric, but a targeted task does not authorize repo-wide
  cleanup. Recommend wider migrations separately and apply them only when authorized.
