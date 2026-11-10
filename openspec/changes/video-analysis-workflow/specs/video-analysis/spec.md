# Video analysis

## Purpose

Provide goal-directed audiovisual findings with traceable evidence and explicit coverage
limitations.

## ADDED Requirements

### Requirement: Evidence-aware analysis

The workflow SHALL distinguish captured, processed, inspected, inferred, and externally
corroborated information.

#### Scenario: Sampled recorded video

- **WHEN** a user requests analysis of a bounded YouTube excerpt
- **THEN** findings identify their evidence and timing basis
- **AND** coverage gaps and uninspected modalities remain explicit

### Requirement: Bounded live workflow

The workflow SHALL separate segmented capture from analysis and require explicit time and storage
limits.

#### Scenario: Interrupted broadcast

- **WHEN** capture encounters a transient interruption
- **THEN** recovery checks use the agreed interval and deadline
- **AND** resumed capture preserves completed segments and records uncertain gaps

#### Scenario: Storage pressure

- **WHEN** capture reaches its storage limit or free-space reserve
- **THEN** capture stops safely without silently deleting unprocessed evidence

### Requirement: Layered delivery

The workflow SHALL deliver the agreed answer before supporting evidence and optional retained
artifacts.

#### Scenario: Noncommercial question

- **WHEN** a user asks about a lecture or visual technique
- **THEN** the brief answers that question without mandatory business opportunities or experiments
