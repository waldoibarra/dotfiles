# Spec Delta

## Purpose

Prevent unsupported live recovery from overwriting retained evidence or claiming continuous coverage.

## ADDED Requirements

### Requirement: Safe default recovery

The recorder MUST retain prior files unchanged and stop partial after downloader failure.
It MUST NOT repeat a from-start invocation automatically.

#### Scenario: First downloader failure

- **WHEN** the initial downloader fails
- **THEN** retained files remain unchanged and the default terminal status is partial

### Requirement: No lossy fallback

The recorder MUST retain the initial segment and stop partial after failure.
It MUST NOT retry after cancellation, limits, or access restrictions.

#### Scenario: A bounded stop occurs

- **WHEN** cancellation, disk reserve, byte budget, or access restriction stops capture
- **THEN** the recorder records a terminal result without another downloader invocation

### Requirement: Access restrictions stop acquisition

The recorder MUST stop rather than retry with bypass options after access restriction evidence.

#### Scenario: Downloader reports a login wall

- **WHEN** the current downloader attempt reports a login wall, DRM, bot challenge, 401, or 403
- **THEN** the recorder records stopped status without fallback retries
