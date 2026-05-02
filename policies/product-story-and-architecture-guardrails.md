# XRTM Product Story and Architecture Guardrails

This document is the canonical reference for three recurring decisions:

1. when we must rerun stress/release validation
2. when a macro reorganization is required versus unnecessary
3. how we describe XRTM consistently so the story does not drift across repos

It exists to keep architectural and messaging decisions explicit as the stack evolves.

## Current decision

As of 2026-05-02:

- the 4-repo structure is **kept**
- a macro reorganization is **not required now**
- the canonical XRTM story should **not** lead with local-LLM

The current intended repo roles remain:

- `data` — foundational corpus/data layer
- `forecast` — forecasting/runtime library layer
- `xrtm` — product/operator shell
- `xrtm.org` — presentation and documentation layer

## 1. Stress and release rerun policy

### Immediate answer

We do **not** need to rerun the full deep stress campaign after every change.

We **do** need to rerun the right validation tier for the type of change made.

### Required rerun matrix

| Change type | Required rerun |
| --- | --- |
| Docs/site/governance-only changes | Repo-local checks only (`npm run build`, docs build, `git diff --check`, or equivalent) |
| Cross-repo policy / release-train / CI coordination changes | Package-install matrix, cross-repo workspace stress, and proof-point workflow checks |
| Public API or package-boundary changes in `data`, `forecast`, or `xrtm` | Package-install matrix, cross-repo workspace stress, proof-point workflow checks, plus affected repo tests |
| Changes to pipeline, validation, monitoring, history/artifacts, provider behavior, or local-LLM logic | Full affected stress lane(s), including repeated-command stability and any relevant deep runtime checks |
| Release candidate / coordinated release | Full release-train validation matrix from the release-readiness policy |

### Release candidate minimum

Before calling a coordinated release candidate green, rerun at minimum:

1. package-install matrix
2. cross-repo workspace stress
3. official proof-point workflows
4. any deep stress lane directly affected by code changes since the last run

### Full deep stress is mandatory when

Run the full deep stress set again if a change touches any of these:

- corpus loading / registry / validation contracts
- forecast generation pipeline behavior
- provider selection or provider execution behavior
- run artifact creation / reading / export semantics
- monitoring lifecycle or repeated-run stability
- local-LLM harness behavior

If the change is only documentation/policy/presentation, a full rerun is not required.

## 2. Macro reorganization decision rule

### Immediate answer

A macro reorganization is **not needed now**.

### Concrete trigger rule

Start a macro-reorganization plan **only if 3 or more** of the following conditions
occur within the **next 2 coordinated release cycles**:

1. **Unpublished dependency coupling**
   - A release-train PR or release requires unpublished same-branch changes in **3 or more repos** to function.

2. **Branch alias or ref hack recurrence**
   - CI or release validation requires branch aliases, manual upstream ref overrides, or fallback-branch tricks in **2 or more repos**.

3. **Late compatibility failures**
   - Downstream incompatibilities are discovered only at release-train or cross-repo integration time **2 or more times**, after repo-local CI passed.

4. **Feature-spread overload**
   - More than **33% of top-priority user-facing roadmap items** require code changes in **3 or more core repos**.

5. **Clean release impossibility**
   - A coordinated release cannot be cut from clean branches and published artifacts without unpublished sibling branches or hand-carried local state.

6. **Boundary-regression recurrence**
   - We need another structural cleanup pass for the same hotspot categories again:
     - `xrtm` orchestration sprawl
     - `forecast` public API leakage
     - `data/corpora` catch-all pressure

### Decision table

| Result over next 2 release cycles | Decision |
| --- | --- |
| 0-2 trigger conditions hit | Keep the 4-repo structure and continue tightening |
| 3+ trigger conditions hit | Start a macro-reorganization plan |

### What counts as macro reorganization

Examples:

- merging core repos into a monorepo
- merging two of the core repos into one package/repo boundary
- redefining the package/release model so the current repo roles no longer exist as-is

Examples that **do not** count:

- narrower public APIs
- internal module refactors
- better CI/release-train wiring
- stronger compatibility policy
- repo-local boundary tightening

## 3. Canonical XRTM story

### Primary story

XRTM is **AI for event forecasting**.

AI can already generate plausible answers. The bigger opportunity is using AI to
forecast real-world events, keep a durable record of predictions, measure
accuracy, and get better over time.

Its core value loop is:

- forecast real-world events
- track predictions and evidence
- measure accuracy and calibration
- improve the system over time

### Proof/workflow order

All public-facing surfaces should prove that story with these workflows, in this
order:

1. **Provider-free first success**
   - prove the event-forecasting loop quickly
   - no API key
   - deterministic first run

2. **Benchmark and validation workflow**
   - evaluate forecast quality
   - compare runs
   - inspect artifacts and metrics

3. **Monitoring / history / reporting**
   - run recurring workflows
   - inspect changes over time
   - export decision-friendly artifacts

4. **Local-LLM advanced path**
   - advanced capability
   - privacy/local-control story
   - power-user path

### Local-LLM positioning rule

Local-LLM is an **advanced differentiator**, not the primary hook.

That means:

- it should **not** be the first sentence of the README hero or site hero
- it should **not** be the default explanation of what XRTM is
- it **should** appear as the advanced path once the core product story is already clear

### Messaging rule

If a page has only one short explanation of XRTM, it should say some version of:

> XRTM is AI for event forecasting. It helps teams forecast real-world events,
> track predictions, measure accuracy, and improve over time.

### Page-role rule

Do not make every page repeat the same paragraph. The message should stay
recognizable, but each page must do a distinct job:

- **hero / homepage**: category statement
- **intro / getting started**: why now and the first value loop
- **workflow pages**: proof
- **package READMEs**: package role inside the system
- **governance docs**: canonical wording and anti-drift policy

### Anti-drift rule

The following repos own the following truths:

- `governance` owns policy, compatibility, and canonical architectural guardrails
- `data`, `forecast`, and `xrtm` own product/package behavior in their domains
- `xrtm.org` explains and presents the ecosystem, but does not become the only authority

If site/docs copy a policy or architecture claim, they must link back to the
canonical owner. Keep category wording aligned, but let each page contribute a
different layer of the story instead of forcing slogan repetition.

## Review cadence

Re-check this document:

- before each coordinated release
- after each release retrospective
- before any proposal to merge or split core repos

If the decision changes, update this file first, then update downstream docs.
