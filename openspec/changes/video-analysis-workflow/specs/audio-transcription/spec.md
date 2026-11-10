# Audio transcription

## Purpose

Produce independent local speech transcripts with original-language wording and honest processing coverage.

## ADDED Requirements

### Requirement: Independent transcription

The workflow SHALL select a fitting local speech model and preserve source provenance and uncertainty.

#### Scenario: Unknown spoken language

- **WHEN** source language has not been established
- **THEN** transcription uses language detection instead of an inferred English hint
- **AND** captions are not substituted silently

### Requirement: Honest timing and completeness

The workflow SHALL distinguish chunk timing from aligned word or utterance timestamps.

#### Scenario: Chunk-only timing

- **WHEN** a recognizer returns text with only chunk bounds
- **THEN** citations use those ranges without invented sentence timestamps

#### Scenario: Missing prerequisites

- **WHEN** an authorized run lacks a runtime or cached model
- **THEN** the agent reports the prerequisite and requests installation authorization
- **AND** partial output is not presented as a complete transcript
