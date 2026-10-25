# Harness change workflow

## Purpose

Let shared coding harnesses plan, approve, and resume scoped changes without relying on private chat
history.

## ADDED Requirements

### Requirement: Approval precedes implementation

Agents MUST refine tasks and present plans before implementation, unless the user explicitly waives
planning.

#### Scenario: Feedback on a proposal

- **WHEN** the user requests changes to a proposed plan
- **THEN** the agent revises the plan without starting implementation

#### Scenario: Approved scope changes

- **WHEN** implementation requires a material scope change
- **THEN** the agent requests approval before executing that change

### Requirement: Shared skills-only delivery

Workstation synchronization SHALL deliver the OpenSpec CLI and shared upstream skills without
requiring slash-command invocation.

#### Scenario: Second workstation setup

- **WHEN** a collaborator synchronizes the same dotfiles revision
- **THEN** the CLI and skills-only configuration are available through the declared delivery
  mechanism

#### Scenario: Unchanged skill generation

- **WHEN** the installed CLI reports no generated-skill changes
- **THEN** synchronization leaves those generated files unchanged

### Requirement: Portable change state

Collaborating agents MUST use the same approved change and explicit repository revision.

#### Scenario: Parallel implementation

- **WHEN** two agents implement separate approved tasks concurrently
- **THEN** their writes are isolated and the lead integrates results into the canonical change

### Requirement: Authored artifacts follow shared rules

Authored OpenSpec artifacts MUST follow shared communication, documentation, and
evidence-preservation rules.

#### Scenario: Removing obsolete guidance

- **WHEN** an approved refactor supersedes operational guidance
- **THEN** affected instructions and links are updated while consequential rationale and protected
  evidence remain available
