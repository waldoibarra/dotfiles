# Spec Delta

## Purpose

Provide bounded local livestream capture that preserves usable partial evidence under failures.

## ADDED Requirements

### Requirement: Bounded capture agreement

The recorder MUST persist a unique agreement before starting any downloader child.
It MUST reject non-finite resource limits and existing run directories.

#### Scenario: Valid bounded invocation

- **WHEN** an operator supplies a new run directory and finite limits
- **THEN** the recorder writes agreement, event, and atomic status records

### Requirement: Owned child supervision

The recorder MUST terminate its owned process group on cancellation, deadline, stall, disk, or byte
limits.

#### Scenario: A child stalls

- **WHEN** one selected track receives no verified byte growth within its stall limit
- **THEN** the recorder terminates owned children and records a partial result

#### Scenario: A combined output hides selected-track progress

- **WHEN** combined output grows before both selected tracks show verified progress
- **THEN** the recorder stops partial instead of inferring per-track continuity

#### Scenario: Combined output coexists with a stalled selected track

- **WHEN** one selected track freezes while another grows, regardless of combined-media progress
- **THEN** the recorder stops partial for the selected-track stall

#### Scenario: Both selected tracks become idle during merge

- **WHEN** both selected tracks previously advanced and combined media keeps growing
- **THEN** merge progress prevents a false stall within resource limits

### Requirement: Accurate terminal status

The recorder MUST report `complete` only after fresh source-end confirmation and probe evidence.
It MUST separately decode audio and video before reporting `complete`.
It MUST report sampled decode duration and leave broadcast completeness unknown.
It MUST report a gapped run as `partial`.

#### Scenario: Capture ends without media verification

- **WHEN** a downloader exits without successful probe and decode checks
- **THEN** the status is partial and records the failed verification
