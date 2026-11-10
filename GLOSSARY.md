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

**Prototype**:
A disposable artifact or experience answering a bounded question without committing to production
implementation.

**Proof of concept (POC)**:
A prototype focused on whether a capability or approach is feasible under stated conditions.

**Ambition**:
Seeking materially better outcomes through stronger methods, reframed approaches, or
cross-disciplinary possibilities within authorized boundaries.

**Gamification**:
Game-design elements applied to a non-game activity to influence the experience or behavior.
_Avoid_: Proof of user benefit or commercial success.

**Durable change**:
An approved modification intended to remain maintained after the session.

**Workflow schema**:
An OpenSpec definition of change artifacts, their dependencies, and implementation task tracking.

**Evolutionary architecture**:
An architectural approach supporting guided, incremental change across technical, domain, data,
and operational dimensions.
Feedback and fitness functions protect important architectural characteristics as the system evolves.

**Architectural fitness function**:
An objective assessment of whether a system preserves a chosen architectural characteristic as it
changes.
Examples include checks of security, performance, modularity, and data integrity.

Source: [Building Evolutionary Architectures](https://evolutionaryarchitecture.com/precis.html).

## Media analysis

**Video analysis**:
Goal-directed interpretation of relevant spoken, visual, and non-speech audio content.
_Avoid_: Intelligence extraction, when implying independently verified truth.

**Evidence item**:
A source-linked observation supporting or challenging an analytical finding.

**Finding**:
A conclusion drawn from identified evidence, with its uncertainty stated.

**Analysis brief**:
The reader-facing synthesis answering an agreed question through findings, evidence, and limitations.

**Capture coverage**:
The source intervals and modalities successfully retained as usable media.
_Avoid_: Analysis coverage, when only acquisition is established.

**Analysis coverage**:
The intervals and modalities actually inspected for the agreed question.
_Avoid_: Full viewing, when only sampled frames or speech were inspected.

**Coverage record**:
An account of capture, processing, and inspection coverage, including omissions and failures.

**Near-live analysis**:
Interpretation of completed media segments while a broadcast continues.
_Avoid_: Real-time analysis, when processing introduces material delay.

## Agent coordination

Terms for coordinating agents across harnesses; the
[agent coordination manual](/docs/ai-harness/agent-coordination/README.md) owns the procedures.

**Operator**:
The human directing agent work and granting its authority.
_Avoid_: Captain; administrator, when referring to task authority rather than system administration.

**Lead**:
The agent responsible for coordinating an approved scope and returning its outcome to the operator.
_Avoid_: First mate, primary, orchestrator worker.

**Worker**:
An agent assigned a bounded task, with explicit authority and completion criteria, reporting to a
lead.
_Avoid_: Crewmate; subagent, unless describing the actual runtime relationship.

**Delegated lead**:
A persistent worker assigned responsibility for coordinating its own team within a parent lead's
authorized scope.
_Avoid_: Secondmate; remote lead, unless its location is specifically relevant.

**Team**:
A lead and the workers coordinated within its assigned scope.
_Avoid_: Crew, fleet, swarm.

**Delivery task**:
An assignment whose required outcome is an authorized change delivered through the project's
agreed delivery process.
_Avoid_: Ship task; implementation task, when delivery includes documentation or configuration.

**Investigation task**:
An assignment whose required outcome is a standalone findings report, not a delivered project
change.
_Avoid_: Scout task; read-only task, because producing the report itself requires writing.

**Peer agent**:
An agent collaborating with another agent without reporting to it for the relevant scope.
_Avoid_: Teammate, when used to imply equal authority; worker, when no reporting relationship
exists.

**Independent reviewer**:
An agent assessing a plan or result without having produced the material being reviewed.
_Avoid_: Peer reviewer, when equal authority is neither required nor established.

**Subagent**:
An agent invoked through a harness's native delegation mechanism to perform work for a calling
agent.
_Avoid_: Worker, when the distinction concerns runtime rather than responsibility.

**Task brief**:
The contract defining an assignment's goal, boundaries, authority, expected deliverable, and
completion criteria.
_Avoid_: Prompt, when referring to the complete assignment contract rather than its transmission.

**Task record**:
The durable account of an assignment's brief, ownership, state, evidence, and unresolved
obligations.
_Avoid_: Chat history; task brief, when referring to execution state.

**Supervision**:
The continuing oversight that reconciles task records with observed execution and identifies
required intervention.
_Avoid_: Monitoring, when oversight also includes decisions and recovery.

**Escalation**:
A request to the responsible authority for a decision outside the requesting agent's granted
authority.
_Avoid_: Progress update; human escalation, unless the required authority is the operator.

**Task worktree**:
A separate Git working tree assigned to a task to isolate its file edits from concurrent work.
_Avoid_: Sandbox, when implying isolation of credentials, processes, or external side effects.

Sources: [firstmate vision](https://github.com/kunchenguid/firstmate/blob/main/VISION.md) and
[Claude Code agent teams](https://code.claude.com/docs/en/agent-teams), with the sailing metaphor
replaced by role names.
