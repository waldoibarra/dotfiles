# Documentation information architecture

**Information architecture connects concerns, reader needs, and the routes between them.**
Directories express responsibility and ownership; overview pages explain meaning and relationships.
Diátaxis distinguishes page purposes; progressive disclosure makes further detail available when
needed.
The directory layout represents these choices without defining them.
Ordinary Markdown is sufficient; no documentation generator is required.

**Use this as guidance and inspiration, not a universal architecture or mandatory directory tree.**
Adapt it to the project's size, audience, domain, lifecycle, and existing documentation contracts.
Use only the layers and page types that help readers; omit unnecessary structure.
Safety, factual accuracy, and approval boundaries still apply.

## Contents

- [Concerns and ownership](#map-concerns-before-paths)
- [Page purpose with Diátaxis](#choose-page-purpose-with-diátaxis)
- [Progressive disclosure](#choose-useful-reading-layers)
- [Relationships and navigation](#connect-the-layers)
- [Reader-route checks](#check-reader-routes)

## Map concerns before paths

- Establish the system's purpose, audience, boundaries, and representative flows from verified
  evidence.
- Identify each concern's responsibility, canonical owner, readers, and questions.
- Group meaningful systems and workflows; do not mechanically mirror source directories.
- Separate explanation, procedures, reference facts, and historical evidence when their reading
  needs differ.
- Keep current behavior, accepted future work, and historical outcomes distinguishable.

## Choose page purpose with Diátaxis

[Diátaxis](https://diataxis.fr/) distinguishes documentation by reader need, not by topic or
directory depth.
Its [compass](https://diataxis.fr/compass/) separates doing from understanding, and learning from
applying existing skills.

| Page purpose | Reader need | Lead with | Keep separately linked |
| --- | --- | --- | --- |
| Tutorial | Learn through guided practice | Learning outcome, prerequisites, supported steps | Unnecessary alternatives and extended theory |
| How-to guide | Accomplish a specific task | Goal, prerequisites, actionable steps | Lessons and architectural background |
| Reference | Look up precise information | Facts, contracts, settings, or interfaces | Walkthroughs and explanatory essays |
| Explanation | Understand concepts and decisions | The question, its answer, context, and reasoning | Operational procedures and exhaustive specifications |

**Concern, page purpose, and reading depth are independent choices.**
A single concern may need several page purposes; none requires four folders or four documents.
A tutorial can be introductory or advanced; reference material need not sit at the deepest level.
Choose one primary purpose per page and link supporting material rather than mixing extended
treatments.
Retain prerequisites, safety conditions, and brief context needed to use that page correctly.

An overview can orient readers and route them to several page purposes without becoming a
comprehensive manual.
Plans, glossaries, instruction files, and skill entrypoints retain their own artifact contracts.
Use Diátaxis where it clarifies reader needs; do not force every artifact into a quadrant.

## Choose useful reading layers

| Layer | Reader's question | Content |
| --- | --- | --- |
| System orientation | What is this, and how does it fit together? | Purpose, boundaries, major relationships, reading routes |
| Concern overview | How does this area work? | Responsibility, interfaces, main flow, constraints, linked detail |
| Focused detail | What do I need for this task? | Procedures, contracts, configuration, mechanisms, failure recovery |

**These are reading layers, not mandatory directory levels or page templates.**
A small guide can provide them through headings and links.
Create a directory only when a distinct concern needs multiple pages.
Split by reader need, ownership, or change lifecycle; page length alone is not a reason.

**Overviews explain; indexes help locate.**
Explain purpose and boundaries in orientation pages instead of opening with a file inventory.
Do not make every how-to or reference page begin with an architectural explanation.
Lead with what that page's reader needs; link broader context without requiring a sequential reading
path.
Use diagrams when they clarify boundaries or flows, not merely to redraw the directory tree.
Keep generated indexes under their publisher's ownership; author explanations in maintained pages.

## Connect the layers

- Give each fact or procedure one canonical home; summarize briefly elsewhere and link to it.
- Describe links by reading need, such as “Read session recovery when login succeeds but requests
  fail.”
- Provide direct routes to common procedures; experienced readers need not traverse every overview.
- Link conceptual neighbors and cross-concern flows, including the relevant interfaces and state
  owners.
- Explain interactions in workflow pages without copying each concern's detailed contract.
- Link focused pages back to context when breadcrumbs or existing navigation do not provide it.

## Check reader routes

Use the touched pages and their necessary links to answer the applicable questions:

1. Can the entrypoint explain the system's purpose, boundaries, and major relationships?
2. Can a reader reach a specific procedure without reading every overview?
3. Can a reader trace one interaction across concern boundaries?
4. Can a maintainer update one fact at its canonical owner without editing competing copies?
5. Does each page serve its primary reader need without becoming a lesson, manual, and reference
    simultaneously?
6. Can readers choose explanation, practice, action, or lookup without mandatory traversal through
    the other purposes?

The `docs` workflow owns preservation, authorization, and implementation checks.
These questions evaluate navigation and purpose; they do not require adding missing document
categories.

**Evidence:** Report inspected routes, broken links, and unresolved context separately from
formatting results.
Authored scenarios, installed instructions, and passing lint do not establish successful reader or
agent behavior.
