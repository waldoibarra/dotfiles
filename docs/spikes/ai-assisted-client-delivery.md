# Evidence for a risk-scaled delivery process

This dated research supports the [current project-delivery guide](/docs/project-delivery/README.md).
It does not establish universal outcomes or binding policy.

Accessed **2026-11-06**. These are opened primary sources, not search excerpts.
They support practices, not guaranteed outcomes. Client evidence remains outside
this reusable file.

## Lifecycle and experiments

- [GOV.UK discovery][source-1] begins with users, constraints, and a go/no-go
  decision. Its typical four-to-eight-week discovery describes government
  services, not a consultant's required duration.
- [GOV.UK alpha][source-2] tests risky assumptions with disposable prototypes.
  It explicitly permits discarding code and stopping before alpha.
- [GOV.UK beta][source-3] pilots real use before wider release and gathers
  outcome data. [Live guidance][source-4] adds sustained support, monitoring,
  security, and training. Government assessment and public-access obligations do
  not automatically apply to private client work.
- [GitHub Spec Kit](https://github.com/github/spec-kit) offers independent
  entrypoints for specification-driven development, bug fixing, and idea
  assessment. [GitHub's SDD explanation][source-5] makes specifications central
  to implementation. Those are vendor methods, not evidence that every task
  needs a PRD or that specifications guarantee quality.

## Secure AI work and empirical limits

- [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) describes
  high-level secure practices integrated into any SDLC. It is not a
  certification or proof of an application's security.
- [Claude Code best practices][source-6] distinguishes model-followed
  instructions from enforceable controls. Its examples include tests,
  permissions, and spending limits; these features depend on the installed tool.
- [DORA 2024](https://dora.dev/research/2024/dora-report/) reports increased
  individual productivity alongside reduced delivery stability and throughput.
  This survey-level association does not predict a project's result or identify
  a causal effect here.
- [METR's randomized early-2025 study][source-7] assigned real repository tasks
  to AI-allowed or disallowed conditions. Sixteen experienced developers took
  19% longer with AI on studied tasks. Results concern specific developers,
  repositories, tasks, and tools; do not generalize to every project.
- [METR's February 2026 update][source-8] warns that its earlier slowdown is
  outdated. Its later samples suggest possible speedups, but selection and
  timing biases prevent reliable size estimates. Therefore measure local task
  outcomes instead of selling assumed acceleration.

## Terminology and evidence gaps

[AWS defines AI-DLC][source-9] as AI-Driven Development Life Cycle. Its three
phases are Inception, Construction, and Operations, with human validation of
critical decisions. [AWS Labs' implementation][source-10] describes five phases,
including Initialization and Ideation. Its [workflow profiles][source-11] vary
the number of executed stages and their depth.

[The ADLC toolkit author][source-12] calls ADLC the Agentic Development
Lifecycle. Its [thesis][source-13] proposes gates addressing model failure
modes. This is a first-party project definition, not evidence of industry
consensus or validated productivity claims. AI-DLC and this ADLC name different
methods; neither replaces commercial and client-operational decisions. No
primary empirical evidence opened here proves a particular commercial payment
schedule or acceptance window improves outcomes. Those remain proposed
negotiating defaults requiring local counsel.

**Failure patterns:** Do not treat vendor inventories as client commitments. Do
not promote demos without recovery testing. Check negative behavior before
trusting generated tests. These are risk judgments derived from the cited
lifecycle and security guidance, not measured rates.

[source-1]: https://www.gov.uk/service-manual/agile-delivery/how-the-discovery-phase-works
[source-2]: https://www.gov.uk/service-manual/agile-delivery/how-the-alpha-phase-works
[source-3]: https://www.gov.uk/service-manual/agile-delivery/how-the-beta-phase-works
[source-4]: https://www.gov.uk/service-manual/agile-delivery/how-the-live-phase-works
[source-5]: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
[source-6]: https://code.claude.com/docs/en/best-practices
[source-7]: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
[source-8]: https://metr.org/blog/2026-02-24-uplift-update/
[source-9]: https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/
[source-10]: https://github.com/awslabs/aidlc-workflows/blob/main/docs/guide/04-phases-and-stages.md
[source-11]: https://github.com/awslabs/aidlc-workflows/blob/main/docs/guide/workflow-profiles.md
[source-12]: https://github.com/voodootikigod/adlc/blob/main/README.md
[source-13]: https://github.com/voodootikigod/adlc/blob/main/ADLC.md
