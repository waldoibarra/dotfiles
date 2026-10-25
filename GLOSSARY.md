# Dotfiles language

Terms used to configure and maintain this workstation and its AI harness.

## Language

**Intent clarification**:
The harness's analysis of a request's outcome, target, boundaries, assumptions, and communication
circumstances.
_Avoid_: Four dimensions of intent, when implying a universal or established framework.

**Goal**:
The outcome that makes the requested response or action useful.

**Constraint**:
A condition the requested response or action must satisfy.

**Assumption**:
A belief treated as true without sufficient confirmation for the current task.
_Avoid_: Requirement, when the user has not established a constraint.

**Target**:
The specific subject, artifact, version, or decision addressed by a request.
_Avoid_: Entity, when referring to the object of a harness request.

**Audience analysis**:
Identification of intended readers, their existing knowledge, and the information they need.

**Rhetorical situation**:
The circumstances of communication, described through text, author, audience, purposes, and setting.

**Feedback loop**:
Comparison of intended and observed outcomes used to assess subsequent adjustments.
The harness's feedback-loop skill provides assessments and proposals, not automatic modifications.

**Harness**:
The client environment connecting a model with instructions, tools, permissions, and
session state.

**Global contract**:
Shared behavioral instructions that apply across configured clients and
repositories.
_Avoid_: Global memory, when referring to instructions.

**Skill**:
A task-triggered procedure with its own supporting references and checks.

**Role**:
A bounded responsibility with explicit inputs, authority, and completion criteria.

**Lead session**:
The conversation retaining user decisions, coordination, shared processes, and Git
delivery.
_Avoid_: Orchestrator worker.

**Information architecture (IA)**:
Organization, naming, and relationships that make information
understandable and findable.
Use “documentation information architecture” when distinguishing documentation from other
information systems.

**Progressive disclosure**:
Presenting essential information first, with additional detail available
when readers need it.

**Directory layout**:
The physical arrangement of directories and files, representing one aspect of
information architecture.
_Avoid_: Dirs/files architecture, when referring to information organization beyond filesystem paths.

**Canonical source**:
The maintained owner of a fact or rule; other locations point to it.

**Shared memory**:
Durable, scoped knowledge retained in repository documentation or the shared life
vault.
_Avoid_: Chat history, when referring to maintained knowledge.

**Context**:
Information selected for the model's current task, including retrieved memory and fresh
evidence.

**Current guidance**:
Instructions or facts verified as applicable to the present task and scope.

**Historical evidence**:
Retained information explaining past decisions without authorizing their
reuse or execution.

**Managed link**:
An installed symlink whose target is a tracked source.

**Managed copy**:
An installed regular file refreshed from a tracked source by the updater.

**Rendered rule**:
A client instruction file generated from its template and the shared global
contract.

**Workstation sync**:
The authorized update workflow for packages, links, client configuration, and
selected integrations.

**Evolutionary architecture**:
Deliberate structural change guided by feedback, preserved
boundaries, and observable checks.
