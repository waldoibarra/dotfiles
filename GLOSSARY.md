# Dotfiles language

**Purpose:** Define the terms used to configure and maintain this workstation and its AI harness.

## Language

**Harness:** The client environment connecting a model with instructions, tools, permissions, and
session state.

**Global contract:** Shared behavioral instructions that apply across configured clients and
repositories.
_Avoid_: Global memory, when referring to instructions.

**Skill:** A task-triggered procedure with its own supporting references and checks.

**Role:** A bounded responsibility with explicit inputs, authority, and completion criteria.

**Lead session:** The conversation retaining user decisions, coordination, shared processes, and Git
delivery.
_Avoid_: Orchestrator worker.

**Canonical source:** The maintained owner of a fact or rule; other locations point to it.

**Shared memory:** Durable, scoped knowledge retained in repository documentation or the shared life
vault.
_Avoid_: Chat history, when referring to maintained knowledge.

**Context:** Information selected for the model's current task, including retrieved memory and fresh
evidence.

**Current guidance:** Instructions or facts verified as applicable to the present task and scope.

**Historical evidence:** Retained information explaining past decisions without authorizing their
reuse or execution.

**Managed link:** An installed symlink whose target is a tracked source.

**Managed copy:** An installed regular file refreshed from a tracked source by the updater.

**Rendered rule:** A client instruction file generated from its template and the shared global
contract.

**Workstation sync:** The authorized update workflow for packages, links, client configuration, and
selected integrations.

**Evolutionary architecture:** Deliberate structural change guided by feedback, preserved
boundaries, and observable checks.
