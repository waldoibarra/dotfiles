---
name: shell-scripting
description: >-
  Write, audit, fix, update, or review Bash and POSIX shell scripts for their target
  runtime. Use when working on *.sh files or shell-shebang executables, including
  installers, wrappers, CI scripts, hooks, and entrypoints; or changing portability,
  strict mode, quoting, pipelines, shebangs, and variable declarations.
---

# Shell Scripting

Write, review, or repair scripts for their actual runtime. Work only on the scripts the user
named unless they requested a repository-wide audit. Review mode reports findings without edits.

## Load the rubric

Resolve these paths from this installed skill directory:

| Read when | File |
| --- | --- |
| Before writing, editing, auditing, or fixing a script | [Operational checklist](references/checklist.md) |
| A checklist item needs upstream rationale or an unlisted edge case | [Google Shell Style Guide](references/google-shell-style-guide.md) |
| Creating a script with useful helper functions | [Structured Bash template](assets/template.sh) |
| Creating a short, linear script without functions | [Linear Bash template](assets/template-linear.sh) |

The checklist owns the rules, examples, and deliberate Google deviations. It wins when the
verbatim guide disagrees; use the guide where the checklist is silent. Load templates only for
creation, and adapt them to the target rather than copying Bash syntax into a POSIX script.

## Establish the target

Read the shebang, deployment configuration, and project requirements before choosing features.
If a material target constraint remains unknown, ask rather than silently assuming.

- **Shell and version:** a minimal Alpine image normally provides BusyBox `ash`; Bash requires
  explicit installation. macOS's bundled `/bin/bash` is 3.2; `#!/usr/bin/env bash` selects the
  first Bash on `PATH`, not necessarily a newer one. Associative arrays, `${var^^}`, and
  `mapfile`/`readarray` need Bash 4+.
- **Command implementations:** macOS commonly supplies BSD utilities; Linux images may supply
  GNU or BusyBox tools. Flags such as `sed -i`, `date` options, and `readlink -f` vary by
  implementation and OS release. Check the supported target, not a blanket macOS/Linux rule.
- **Architecture:** Homebrew's default prefix is `/opt/homebrew` on Apple Silicon and
  `/usr/local` on Intel macOS. A fixed path is a defect only if it conflicts with the declared
  target. For multiple architectures, detect the prefix with `brew --prefix`; for an unstated
  target, report the assumption.
- **Dialect:** the checklist and templates default to Bash. For POSIX `sh`, use portable
  syntax and options supported by the target shell. Do not import `[[ ]]`, arrays, `local`,
  process substitution, `BASH_SOURCE`, or an unsupported `pipefail` option.

## Detect project conventions

Read `.editorconfig`, `.shellcheckrc`, and the surrounding code. Match neutral choices such as
indentation, width, quoting style, file-name case, and `function` usage. When none exist, use
the checklist defaults; offer a configuration file only if it helps the requested work.

Keep correctness failures separate from house-policy findings. The checklist requires strict
mode for standalone Bash executables, headers for every function except `main`, and no
leading-underscore private markers. Report violations in the requested scope even when
siblings share them, but do not turn a targeted fix into an unrequested convention migration.

## Choose the mode

### Audit

1. Run ShellCheck using the target dialect and repository configuration. It is the mechanical
    floor, not proof of correctness. Report if the tool is unavailable.
2. Walk all ten checklist sections against the requested scripts. Include file naming (§8),
    every non-`main` function's header (§4), strict-mode failure paths (§3), and portability.
3. Report `file:line: issue; impact; fix`, ordered by correctness, portability, then style.
    Distinguish technical defects from the checklist's house policies.

### Fix

Audit, apply the in-scope fixes, and re-run ShellCheck. Match further verification to the
script's effects:

- Safe, read-only scripts: exercise the real path.
- Scripts that install packages, use `sudo`, write system files, remove files, change shells,
  or mutate network/services: do not execute them on the user's machine just to verify.
  Use ShellCheck, syntax checking (`bash -n` for Bash, the target shell's equivalent for `sh`),
  and source inspection. Isolate any necessary runtime check in a disposable environment;
  a dry run establishes only the behavior it actually exercises.

Resolve each finding from the audit explicitly before reporting completion. If a remedy needs
a wider convention migration, report that scope separately; apply it only when authorized.

### Update

Make the requested behavior change using the checklist and detected conventions. Do not
reformat unrelated code. Use the same effect-aware verification boundary as Fix.

### Create

Choose the linear template unless helpers earn their place through reuse, a distinct named
step, or a testing boundary. The checklist's structure rubric (§8) determines helper order
and when `main` is needed. Both templates enable Bash strict mode; the structured template's
guard skips `main` when sourced but does not prevent its top-level options and constants
from affecting the caller. Source it only in an isolated test shell, or extract a library
that follows the sourced-file contract.

Adapt the template to the target, then apply the checklist and effect-aware verification.
If the script grows past roughly 100 lines or needs non-trivial data structures/control flow,
recommend a more suitable language rather than expanding the shell design unquestioningly.

## Report

For changes, summarize the behavior changed, findings resolved, checks actually performed,
and remaining runtime or portability limits. For audit-only requests, return located findings;
do not imply that suggested fixes or unrun checks were completed.
