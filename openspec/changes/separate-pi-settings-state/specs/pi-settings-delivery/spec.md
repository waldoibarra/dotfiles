# Spec Delta

## Purpose

Keep portable Pi defaults versioned while preserving writable runtime state outside the repository.

## ADDED Requirements

### Requirement: Local writable settings

Settings delivery SHALL preserve unspecified local keys and replace values for tracked top-level
keys.

#### Scenario: Upgrade bookkeeping

- **WHEN** Pi updates its local changelog marker after settings delivery
- **THEN** tracked settings remain unchanged

#### Scenario: Managed preferences

- **WHEN** tracked nested preferences or package arrays change
- **THEN** matching local top-level values are replaced completely
- **AND** unrelated local keys remain unchanged

### Requirement: Safe repeatable delivery

Delivery SHALL preserve source files, reject invalid input, and avoid rewriting unchanged regular
files.

#### Scenario: Existing symlink

- **WHEN** the installed settings link points to the tracked source
- **THEN** delivery replaces the link with a regular file while preserving current runtime keys
- **AND** the source remains unchanged

#### Scenario: Repeated sync

- **WHEN** effective settings and permissions already match
- **THEN** bytes, permissions, and modification time remain unchanged

#### Scenario: Invalid or busy destination

- **WHEN** settings are malformed, externally linked, or locked
- **THEN** delivery fails without replacing settings or their source

### Requirement: Discoverable editing procedure

Existing Pi documentation SHALL route maintainers to the canonical source and targeted delivery
procedure.

#### Scenario: Fresh-session settings request

- **WHEN** a maintainer follows repository instructions through the Pi configuration guide
- **THEN** they find source ownership, merge semantics, delivery, reload, verification, and
  recovery guidance
