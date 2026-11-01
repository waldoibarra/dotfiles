# Shared skill reconciliation

## Purpose

Deliver declared shared skills across both workstations without versioning mutable installation state.

## ADDED Requirements

### Requirement: Declarative shared enrollment

The system SHALL install declared external skills for Pi, Claude Code, and Cursor through `dots`.

#### Scenario: New shared skill

- **WHEN** an approved skill declaration reaches the other machine through the shared repository
- **THEN** its next successful `dots` run makes that skill discoverable by all three clients

#### Scenario: Local experiment

- **WHEN** a locally installed skill has no shared declaration
- **THEN** synchronization preserves its installation without enrolling it in the shared manifest

#### Scenario: Invalid declaration

- **WHEN** declarations contain duplicate names, unsupported targets, or owned-name collisions
- **THEN** reconciliation fails visibly before mutating skill installations

### Requirement: Local generated state

The system SHALL keep resolved skill state and generated OpenSpec skills outside tracked Git content.
Authored OpenSpec specifications, schemas, changes, and configuration SHALL remain tracked.

#### Scenario: Upstream update

- **WHEN** upstream skills or the installed OpenSpec generator change
- **THEN** synchronization refreshes local generated state without committing or pushing skill updates
- **AND** skill reconciliation leaves tracked repository files unchanged

### Requirement: Automatic migration and recovery

The system SHALL migrate existing supported installations without requiring a separate manual command.

#### Scenario: Legacy lockfile link

- **WHEN** `dots` encounters the previous repository-owned lockfile symlink
- **THEN** it preserves readable state in a local regular file before native lockfile writes

#### Scenario: Missing legacy target

- **WHEN** the previous lockfile target is absent or its broken link was cleaned
- **THEN** declarations restore required shared skills without depending on the deleted target

#### Scenario: Unknown destination

- **WHEN** reconciliation encounters an unrelated file or conflicting symlink at an owned destination
- **THEN** it reports the conflict before cleanup or reconciliation can remove or overwrite that content

#### Scenario: Interrupted synchronization

- **WHEN** a failed or interrupted synchronization is retried
- **THEN** it converges without duplicate installations, backups, or declarations

### Requirement: Fixed-input idempotency

Reconciliation SHALL avoid repeated mutations when declarations, upstream inputs,
and desired installed state remain unchanged.

#### Scenario: Repeated synchronization

- **WHEN** `dots` repeats with identical inputs and correct installations
- **THEN** skill contents, timestamps, permissions, and discovery links remain unchanged

#### Scenario: Missing client link

- **WHEN** a declared skill exists but one client's discovery link is missing
- **THEN** synchronization repairs that link without rewriting correct skill content

### Requirement: Generated skill bootstrap

The system SHALL generate required OpenSpec skills before reconciling their client discovery links.

#### Scenario: Fresh checkout

- **WHEN** `dots` runs from a checkout without generated OpenSpec skills
- **THEN** generation and discovery succeed without a preliminary manual installation step

#### Scenario: Initial tool installation

- **WHEN** the standalone dotfiles installer runs before agent provisioning
- **THEN** missing generated skills do not prevent tool bootstrap
- **AND** subsequent `dots` or `just update-ca` completes skill provisioning

### Requirement: Agent enrollment guidance

The repository SHALL provide discoverable instructions for enrolling approved shared skills.

#### Scenario: Fresh agent session

- **WHEN** an agent follows repository guidance to add a global shared skill
- **THEN** it finds the manifest, enrollment procedure, client verification, and publication boundaries
