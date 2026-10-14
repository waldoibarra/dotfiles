# Harness design

Read before changing agent configuration, installing integrations, or promoting reusable harness
rules.

## Assign one owner

- Shared instructions, skills, roles, and references belong in `~/.agents/`.
- Use native discovery, links, or minimal adapters instead of copied policy.
- Keep harness-specific settings, credentials, and runtime state in their native directories.
- Reuse existing mechanisms; add abstractions, generators, or dependencies only for demonstrated
  requirements.
- Keep project/company content in its project or work root.
- Keep operator configuration, usage records, and cross-repository plans in their owning workspace.
- Inspect product documentation and agent records for unrelated operator information before
  publishing.

## Select personal/open-source integrations

- Establish hosting, licensing, cost/quotas, authentication effort, required operations, and target
  clients before installing.
- Reuse settled answers; ask only for missing decisions.
- Check existing and first-party options. Distinguish account-bound connectors from portable
  servers.
- Recommend one verified fit; obtain approval before substituting anything that violates accepted
  constraints.
- Verify actual interfaces; mocked tests alone do not establish compatibility.

## Verify activation

- Report configured, installed, loaded, authenticated, and exercised states separately.
- Verify the running host version and deployment path before claiming readiness.
- Check effective instruction precedence, including overrides, before assuming the shared source
  loaded.
- After instruction changes, inspect a fresh session's context; files and links alone prove no
  loaded behavior.
- Keep maintenance commands in the owning workspace's documentation, not portable runtime
  instructions.
