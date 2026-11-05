# Cursor and Herdr

## Purpose

Maintain Cursor CLI provisioning and native Herdr integration through portable dotfiles declarations.

## ADDED Requirements

### Requirement: Managed Cursor executable

The global Mise configuration SHALL declare Cursor Agent CLI and expose `cursor-agent` after installation.

#### Scenario: Install declared tools

- **WHEN** Mise installs the global tool declarations
- **THEN** `cursor-agent` is available without installing Cursor's editor launcher

### Requirement: Repeat-safe Cursor integration

The updater SHALL reconcile Cursor's native Herdr integration only when both executables are available.
It SHALL preserve unrelated Cursor settings and honor `CURSOR_CONFIG_DIR`.

#### Scenario: Missing prerequisite

- **WHEN** Herdr or `cursor-agent` is unavailable
- **THEN** Cursor integration installation is skipped without creating its configuration directory

#### Scenario: Missing or outdated integration

- **WHEN** both executables exist and the integration is missing or outdated
- **THEN** the updater ensures the configuration directory exists and invokes Herdr's Cursor installer

#### Scenario: Current integration

- **WHEN** Herdr reports the Cursor integration as current
- **THEN** the updater performs no installation or file mutation

#### Scenario: Failed installation

- **WHEN** the native installer fails
- **THEN** the updater reports failure and permits a subsequent retry
