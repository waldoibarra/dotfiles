# Proposal

## Why

Plans and research mixed with harness configuration obscure ownership and make cross-session
handoffs unreliable.
Native OpenSpec provides reviewable change agreements without requiring users to memorize slash
commands.

## What Changes

- Provision the latest OpenSpec CLI through Mise and skills-only preferences through Dotbot.
- Generate upstream skills once and link them into the shared Pi and Claude skill locations.
- Require task refinement, alternatives, and explicit plan approval before implementation.
- Apply communication and documentation rules to authored OpenSpec artifacts.
- Document lead-owned coordination across subagents and Herdr-controlled harnesses.
- Preserve historical records while deferring the full documentation refactor to the next session.

## Capabilities

### New Capabilities

- `harness-change-workflow`: Portable, approval-gated change planning and skills-only OpenSpec
  delivery.

### Modified Capabilities

None; no existing OpenSpec specifications were present.

## Impact

Dotfiles owns configuration, provisioning, shared instructions, tests, and integration
documentation.
The life vault owns clarified Sync verification and Waldo's existing workflow-refinement task.
Company repositories, unrelated settings, and broad cross-repository documentation migration remain
excluded.
