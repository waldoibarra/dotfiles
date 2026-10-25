# Spec Delta

## Purpose

Keep throwaway experiments separate from maintained changes while sharing a concise, portable
planning workflow.

## ADDED Requirements

### Requirement: Prototypes bypass OpenSpec

The harness MUST route prototype requests outside OpenSpec, including requests inside
OpenSpec-enabled projects.

#### Scenario: Throwaway experiment

- **WHEN** the user requests throwaway code to test an idea
- **THEN** the agent agrees on the experiment without creating OpenSpec artifacts

#### Scenario: Production promotion

- **WHEN** a prototype produces useful findings
- **THEN** production implementation requires separate approval for a durable change

### Requirement: Minimal durable-change artifacts

The session workflow SHALL require a proposal and tasks, with specifications only when observable
behavior changes.

#### Scenario: Behavior-preserving maintenance

- **WHEN** a change declares no observable behavior change through native skip_specs metadata
- **THEN** tasks can proceed after the proposal without a specification or separate design document

#### Scenario: Observable behavior changes

- **WHEN** a change introduces observable behavior
- **THEN** native validation requires specification deltas rather than accepting an empty
  specification set

### Requirement: Portable workflow ownership

The schema MUST reference the maintained session guide through a stable installed path.

#### Scenario: Another repository uses the shared schema

- **WHEN** its agents resolve the user-level schema
- **THEN** they can locate the session guide without assuming the repository contains dotfiles
  documentation

### Requirement: Approval remains separate from readiness

The harness MUST distinguish explicit user approval from file existence and native CLI readiness.

#### Scenario: Feedback after planning

- **WHEN** the user requests changes to the plan
- **THEN** the agent revises artifacts without starting implementation

### Requirement: Workflow evolution preserves active changes

Approved schema changes MUST preserve active change compatibility or use a distinct schema name.

#### Scenario: Default schema changes

- **WHEN** a project selects session-workflow for new changes
- **THEN** existing changes retain their recorded schema selection
