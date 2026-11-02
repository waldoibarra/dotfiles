# Claude delegation policy

## Purpose

Keep Claude worker delegation on the shared Herdr coordination path across projects.

## ADDED Requirements

### Requirement: Native subagent denial

Delivered Claude user settings SHALL deny native subagent spawning through `Agent` and legacy `Task`.

#### Scenario: Global delivery

- **WHEN** the coding-agent updater delivers Claude settings
- **THEN** both delegation names are denied without project-specific configuration
- **AND** repeating delivery preserves the same denial

#### Scenario: Unrelated task tools

- **WHEN** the delegation restriction is installed
- **THEN** checklist tools and unrelated permissions remain unchanged

### Requirement: Herdr delegation routing

Claude delegation instructions SHALL route workers through the existing Herdr coordination guide.

#### Scenario: Herdr available

- **WHEN** Claude needs an authorized worker inside Herdr
- **THEN** it follows the coordination guide rather than invoking a native subagent

#### Scenario: Herdr unavailable

- **WHEN** Claude needs delegation outside Herdr
- **THEN** it reports delegation unavailable instead of bypassing the restriction
