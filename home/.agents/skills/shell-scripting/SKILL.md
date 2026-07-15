---
name: shell-scripting
description: >-
  Write, audit, fix, update, or review shell scripts (Bash/sh, *.sh files,
  executables with a shell shebang) to a high standard of correctness,
  portability, and style — grounded in Google's Shell Style Guide plus a few
  deliberate deviations. Use this WHENEVER the task involves shell scripts,
  even when the user doesn't name a style guide: creating a new *.sh script or
  installer/wrapper/CI/hook/entrypoint script; auditing or code-reviewing an
  existing shell script; "harden this bash script", "is this script correct",
  "make this portable", "why does my script fail"; editing shebangs, `set`
  flags, quoting, `[[ ]]`, pipelines, or `local` declarations. Prefer this
  skill over ad-hoc shell knowledge — it encodes correctness traps (like the
  `local x=$(...)` exit-code masking bug) that are easy to miss.
---

# Shell Scripting

Produce and improve shell scripts that are **correct**, **portable to their
actual runtime**, and **stylistically consistent** — following Google's Shell
Style Guide with the deliberate deviations recorded below.

This skill is used by many models, some with weak shell priors. So it is
explicit and explains the _why_ behind each rule: a rule you understand you can
apply to novel code; a rule you merely memorized you will misapply. Read
`references/checklist.md` before auditing or writing — it is the full
operational ruleset. `references/google-shell-style-guide.md` is the verbatim
guide, for deep rationale and edge cases.

## Scope discipline

Work **only on the script(s) the user asked about.** Do NOT scan the whole repo
and "fix everything" unless the user explicitly asks for a full audit. When
writing a new script, apply this skill's rules from the start.

---

## Step 1 — Establish the target environment

Portability is not abstract: it depends on _where the script runs_. Before
deciding a shebang or reaching for a command, know the target. It changes:

- **Shebang & shell**: is Bash even present? (Alpine/Docker ships BusyBox `ash`,
  no Bash — a `bash` script there needs `apk add bash`, or must be POSIX `sh`.)
- **Coreutils flavor**: macOS ships BSD `sed`/`date`/`readlink` (e.g. `sed -i ''`
  needs an argument; no `readlink -f`); Linux ships GNU (`sed -i`, `readlink -f`).
  A script that must run on both should avoid the divergent flags or detect them.
- **Bash version**: macOS `/bin/bash` is frozen at **3.2** (2007). Features like
  `declare -A` (associative arrays), `${var^^}`, and `mapfile`/`readarray` are
  Bash 4+. `#!/usr/bin/env bash` picks up a newer Bash from `PATH` if one is
  installed (e.g. Homebrew's), otherwise resolves to 3.2 on macOS.
- **CPU architecture** (when it matters): arm64 vs x86_64 changes hardcoded
  paths — Homebrew lives at `/opt/homebrew` on Apple Silicon but `/usr/local` on
  Intel. Flag a hardcoded arch-specific path **only when it conflicts with the
  declared target**: if the target is a single architecture, that path is correct,
  not a bug; if the target spans architectures (or is unstated), flag it as an
  assumption to make explicit or detect (`$(brew --prefix)`, `uname -m`).

**If the target isn't clear from context, ASK the user** (macOS or a specific
Linux distro? which architecture? a Docker image — which base?). Don't silently
assume. A wrong assumption here produces a script that works on your machine and
fails on theirs.

---

## Step 2 — Detect the project's conventions

House style is per-project. Before applying this skill's defaults, look for and
follow the project's own rules:

- **`.editorconfig`** → indent style/size, `max_line_length`, final newline,
  trailing whitespace. If it sets `indent_size = 2` and `max_line_length = 100`,
  use those, not this skill's defaults.
- **`.shellcheckrc`** → `shell=` dialect, `external-sources`, `source-path`,
  disabled checks. Honor it.
- **Surrounding code** → _neutral_ choices: indent, `function`-keyword usage,
  quoting style, filename case (kebab vs snake). Match what's there; a diff that
  reformats unrelated lines is noise that hides the real change.

**Convention does not excuse a defect.** Matching the project applies to _neutral_
style choices only. Some things this skill takes a position on are **quality
defects, not conventions** — flag them and recommend a repo-wide cleanup **even
when the whole codebase shares them consistently**:

- the `local x=$(cmd)` (and `local -r`/`readonly`) exit-code masking pattern
- missing `set -euo pipefail` on a standalone executable
- missing function header comments on non-obvious functions
- leading-underscore "private" markers

A defect repeated a dozen times is a dozen defects, not a convention — report it
once as "repo-wide" rather than staying silent. A naive "match surrounding code"
reading gets this wrong.

If **none** of these exist, apply the defaults below — and it's often worth
**offering to create `.editorconfig` and/or `.shellcheckrc`**, so the next
person (or model) inherits an explicit convention instead of guessing.

---

## Default conventions (when the project defines none)

These are this skill's defaults. Some deliberately deviate from Google; the
deviation and its reason are noted so you can explain it.

- **Shebang** — `#!/usr/bin/env bash`.
  _Deviation from Google's `#!/bin/bash`._ Rationale: portability. Bash is not at
  `/bin/bash` on every system (FreeBSD, NixOS), and on macOS `/bin/bash` is the
  frozen 3.2; `env bash` follows `PATH` to a modern Bash when one exists.
  Exception: a strictly POSIX target (e.g. minimal Alpine) → `#!/bin/sh` and no
  bashisms.
- **Strict mode** — standalone executables start with `set -euo pipefail`.
  Google says "use `set`" but doesn't prescribe which options; this skill opts
  into all three, because these are small utilities where failing loudly beats
  limping on. See the guarding technique below — strict mode is only safe once
  you apply it.
- **Sourced libraries** — a file meant to be `source`d has **no shebang and no
  `set`**. It inherits the caller's options; setting its own would surprise the
  caller. (ShellCheck: keep `external-sources=true` / `source-path=SCRIPTDIR`.)
- **Naming** — names must **describe purpose before they satisfy case**: rename
  vague placeholders (`content`, `data`, `tmp`, `result`) to the role they play
  (`sudoers_directive`, `backup_path`), and ensure the name matches the actual
  behavior. **File names** describe the script's job and use **kebab-case**
  (`configure-sudo-credential-cache.sh`, not `run.sh`) — a deliberate deviation from
  Google's `snake_case`. Case for identifiers: `UPPER_SNAKE` for constants and
  exported/global variables; `lower_snake` for functions and variables. Do **not**
  prefix "private" helpers or locals with a leading underscore — Bash has no real
  privacy, so the marker adds noise without meaning. See `references/checklist.md`
  §8 for the full naming rubric.
- **Structure** — only includes, `set`, and constants before functions; then all
  functions. **Introduce a function only when it earns its place**: it's called
  more than once, isolates a distinct nameable step, or must be sourced to be
  tested. Don't wrap a short script's whole linear body in one function just to
  give `main` something to call — keep it flat (no functions, no `main`). It
  follows that a `main` function is required **only when the script defines at
  least one other function**; a short, linear script doesn't need one (Google:
  "for short scripts where it's just a linear flow, `main` is overkill and so is
  not required"). When `main` exists, make it the bottom-most function and **guard
  its execution** so the script stays sourceable (e.g. for testing) without
  running:

  ```bash
  if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
  fi
  ```

  **Order the helpers themselves bottom-up by call depth** — `main`'s direct
  calls sit directly above it in call order, their callees sit above those, and
  so on outward. See `references/checklist.md` §8 for the worked example.
  `source` at the **top level, never inside a function** (see the trap below).
- **Output** — normal status to **STDOUT**; errors and warnings to **STDERR**,
  via an `err()` helper. No decorative emoji — they bury the signal you actually
  need to see. `2>/dev/null` should silence noise and leave real errors visible.
- **Indentation / width** — 2 spaces, no tabs; 100-char lines (wider than
  Google's 80) unless `.editorconfig` says otherwise.

---

## The four modes

### AUDIT (read-only: report, don't edit)

Work in this order:

- **Run ShellCheck first** — it's the mechanical floor and catches the
  well-trodden bugs (unquoted expansions/SC2086, backticks/SC2006, etc.). Don't
  hand-re-derive what it reports; let it do that layer.
- **Then apply the judgment layer** from `references/checklist.md` — walk it
  section by section (§1–§10) against the target file; don't stop once you've
  matched a few familiar patterns. This spans the `local` masking bug,
  shebang/strict-mode policy, sourced-lib exceptions, STDOUT/STDERR
  discipline, structure — **including the script's own file name (§8) and
  function-comment coverage (§4), both easy to skip when you're scanning for
  correctness bugs first** — and portability vs. the Step 1 target.
- **Finally, report each finding** as: `file:line — the issue — why it bites —
  the fix.` Lead with correctness bugs, then portability, then style.

### FIX

Do the AUDIT, then apply the fixes and re-run ShellCheck. Then **verify — but
match the method to the script's blast radius:**

- **Safe / read-only scripts** → exercise the real path; a "fix" you didn't run
  is a guess.
- **Side-effecting scripts** (install packages, `sudo`, write system files, `rm`,
  network or service mutations, `chsh`) → **do NOT execute them to verify.** A
  verification run would mutate the user's machine. Use `shellcheck` + `bash -n` +
  careful reasoning; if a runtime check is genuinely needed, isolate it (container,
  VM, or a dry-run flag). Never mutate the user's environment to test a fix.
- **Before reporting FIX complete, go back through the AUDIT's own findings
  list, one item at a time, and confirm each is actually resolved in the
  diff.** Don't re-derive completeness from a holistic read of the diff or
  from memory — verify against what you yourself already enumerated.
  ShellCheck can't check this; it's a judgment-layer gap, and a holistic read
  is how a finding quietly goes unfixed or gets a half-measure. This is a
  general discipline, not specific to any one category — whatever the AUDIT
  surfaced (correctness, naming, structure, portability, comments, ...) is
  exactly what this final pass checks against.

When a fix is really a **repo-wide convention migration** (dropping `_` prefixes,
removing emoji, adding strict mode, adding function headers), don't silently
diverge one file from its siblings. Flag it as repo-wide and either apply it
across the codebase or confirm the scope with the user — a lone reformatted file
is its own inconsistency.

### UPDATE

Modify an existing script while **matching its detected conventions** (Step 2).
Change what the task needs; don't reformat the rest.

### CREATE

Start from a template, then adapt it to the Step 1 environment and Step 2
conventions:

- `assets/template.sh` — structured: helper functions + a guarded `main`.
- `assets/template-linear.sh` — a short, linear script with no functions (so no
  `main` and no source-guard).

Keep it small — if it's growing past ~100 lines or needs non-trivial data
structures, say so and suggest a real language (Google's own advice).

---

## Non-negotiable correctness traps

These cause silent, wrong behavior and are easy to miss. Never ship them.

- **`local x="$(cmd)"` masks `cmd`'s exit code.** `local`/`declare`/`readonly`
  is itself a command that returns 0, overwriting `$?`. Under `set -e` the
  failure vanishes. **Split it:**

  ```bash
  local x
  x="$(cmd)"          # now $? and set -e see cmd's real result
  ```

  The same masking is why `source` belongs at the top level, not inside a helper
  that resolves its path with `local dir="$(...)"`.
- **Full guarding is a 3-step technique, not just a flag.** To make
  `set -euo pipefail` safe: (1) split every `local x=$(...)`; (2) guard optional
  variables with `${VAR:-}` so `-u` doesn't abort on a legitimately-unset var
  (e.g. `[ -n "${ZSH_VERSION:-}" ]`); (3) then enable the flags. Every script
  _can_ be fully guarded — it just takes these steps.
- **Quote expansions** — `"${var}"`, `"$@"` (not `$*`) — unless you have a
  specific reason not to. Unquoted expansion word-splits and glob-expands.
- **`[[ ]]` over `[ ]`**; `(( ))` for arithmetic (and beware a bare
  `(( i++ ))` returning non-zero under `set -e`).
- **Pipelines/`while read`** — pipes run in a subshell, so variables set inside
  `cmd | while read` don't survive. Use `while read ... done < <(cmd)`.

When the checklist and the verbatim guide disagree with each other, the checklist
wins (it records this repo's deviations); when the checklist is silent, defer to
the verbatim guide.
