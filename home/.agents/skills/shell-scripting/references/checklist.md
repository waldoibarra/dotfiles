# Shell Scripting Checklist

The operational ruleset. Every item is a do/don't with a one-line _why_ and, in
brackets, the section of `google-shell-style-guide.md` to read for full
rationale. **DEVIATION** marks the few places where this skill deliberately
**contradicts an explicit Google rule** (and says why); where Google is merely
silent, a rule carries no such marker — it's just a rule. The checklist wins on
any conflict.

How to use this file:

- **Auditing/fixing?** Walk the sections top to bottom against the target script.
- **Writing new?** Start from `../assets/template.sh`; this file is the rubric.
- Correctness (§Features/Bugs, §Local variables) matters more than style
  (§Formatting). Report and fix in that order.

---

## 1. Which shell & when [§Background]

- Bash for anything non-trivial; POSIX `sh` only when the target forces it
  (minimal Alpine/BusyBox, constrained boot environments). _Why:_ bashisms
  (`[[ ]]`, arrays, `local`) are worth having when Bash is available.
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

- Standalone executables start with `set -euo pipefail`. _Why:_ small utilities
  should fail loudly, not limp on with an unset var or a masked pipe failure.
  Google says "use `set`" but doesn't prescribe which options; this skill opts
  into all three. (Watch the one `set -e` pitfall — bare `(( i++ ))`; see §7.)
- **Sourced libraries: no `set`** (and no shebang). _Why:_ they inherit the
  caller's options; overriding them surprises the caller.
- Strict mode is only safe with the **3-step guarding technique** — see §8.
- Errors/warnings → **STDERR**; normal status → **STDOUT**. Use an `err()`
  helper. _Why:_ lets a caller separate real problems from chatter
  (`2>/dev/null`, `2>&1 | grep`). Keep output plain — no decorative emoji; they
  add noise without signal.

  ```bash
  err() { echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2; }
  ```

## 4. Comments [§Comments]

Google defines four kinds. Use all four.

- **File header** — every file opens with a one-line description of what it does
  (copyright/author optional). _Why:_ the reader knows the script's job before
  reading a line of logic.

  ```bash
  #!/usr/bin/env bash
  #
  # Perform hot backups of Oracle databases.
  ```

- **Function comments** — **DEVIATION:** every function gets a header comment, no
  exceptions — the one carve-out is `main()`, which doesn't need one since it's
  self-evident as the entry point. This drops Google's "obvious and short"
  exception for every other function, since that judgment call produces
  inconsistent results across a session. Describe the API so a caller needn't
  read the body: Description, Globals (used/modified), Arguments, Outputs
  (STDOUT/STDERR), Returns (any status beyond the last command's) — include only
  the sections that apply. _Why:_ the comment is the function's contract.
  **When auditing, flag any function (other than `main`) missing a header even
  if no sibling script has them** — their absence is a gap, not a convention
  (see §10).

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
- **Never `eval`.** _Why:_ unpredictable, unauditable.
- Arrays for lists/flag sets: `flags=(--foo --bar); cmd "${flags[@]}"`. _Why:_
  safe quoting; strings-as-lists force `eval`/nested quotes.
- **Pipes to `while` run in a subshell** — variables set inside don't escape.
  Use `while read -r ... done < <(cmd)` or `readarray`. _Why:_ the classic
  "my variable is empty after the loop" bug.
- Arithmetic: `(( ))` / `$(( ))`, never `let`/`expr`/`$[ ]`. Beware a standalone
  `(( i++ ))` evaluating to 0 → non-zero exit → death under `set -e`.
- No aliases in scripts — use functions.
- **Environment awareness** (portability): avoid GNU-only flags when the target
  includes macOS/BSD (`sed -i` vs `sed -i ''`, `readlink -f`, GNU `date`). Avoid
  Bash-4+ features (`declare -A`, `${var^^}`, `mapfile`) when the target may be
  macOS's Bash 3.2. Detect or ask (SKILL.md Step 1) rather than assume.

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
- Do **not** use a leading underscore to mark "private" helpers or locals. Bash
  has no enforced privacy, so the prefix is decoration that implies a guarantee
  the language doesn't provide — name by role instead. **When auditing, flag an
  existing `_`-prefix convention and recommend removing it repo-wide** — its
  consistency doesn't make it correct (see §10).
- Constants & exported vars: `UPPER_SNAKE`, declared at the top, `readonly`/
  `export`. Set-then-`readonly` is fine for runtime-computed constants.
- `local` for every function variable. _Why:_ avoids leaking into the global
  namespace and clobbering something meaningful.
- **CRITICAL — split declaration from command-substitution assignment.** Applies
  to `local`, `local -r`, `readonly`, `declare`, and `export` alike — each is a
  command that returns 0 and overwrites the substitution's exit code.

  ```bash
  local my_var
  my_var="$(cmd)"     # DO: set -e / $? see cmd's exit code
  # local my_var="$(cmd)"   # DON'T: $? is local's exit (always 0) — failure masked
  ```

  _Why:_ the single most common silently-wrong pattern in "guarded" scripts. **Do
  not lean on ShellCheck here:** SC2155 fires on `local x=$(cmd)` but is **silent
  on the `local -r`/`readonly` form** — catch (and, in FIX mode, split) those by
  hand.
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
- **Guard the `main` call** so the script runs when executed but not when sourced
  (e.g. for testing individual functions). _Why:_ sourcing a script to test one
  function shouldn't trigger its top-level work.

  ```bash
  if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
  fi
  ```

## 9. Calling commands [§Calling Commands]

- Always check return values — `if ! cmd; then err ...; exit 1; fi`, or
  `PIPESTATUS` for a specific stage of a pipe (copy it immediately; `[` clobbers
  it). _Why:_ a command that failed and wasn't checked corrupts later state.
- **Clean up with `trap`.** Register cleanup for temp files/resources so it runs
  on every exit path — including `set -e` aborts and early `return`/`exit`, which
  skip a trailing `rm`: `tmp=$(mktemp); trap 'rm -f "${tmp}"' EXIT`. Use `RETURN`
  for function-scoped resources, `EXIT` for script-scoped. Optionally
  `trap 'err "failed near line ${LINENO}"' ERR` for a diagnostic on abort.
- Prefer Bash builtins / parameter expansion over spawning `sed`/`awk`/`expr` for
  simple string/number work. _Why:_ faster, more robust, fewer portability traps.

## 10. When in doubt [§When in Doubt: Be Consistent]

- Match the surrounding code on **neutral** choices (indent, case, `function`
  keyword) over any personal preference. Consistency is the tie-breaker when
  there's no technical argument.
- **But consistency never excuses a quality defect** the skill takes a position on
  — the `local`-masking pattern, missing strict mode, missing function comments on
  non-obvious functions, leading-underscore "private" markers. Flag these even when
  the whole codebase shares them, and recommend a repo-wide fix. A defect repeated
  consistently is still a defect, not a convention.
