# Stack Versioning Policy

This policy defines how versions work across the XRTM stack. XRTM ships through multiple repositories with different stable surfaces, release cadences, and audiences. Forced lockstep version numbers would hide what actually changed, overstate some releases, and understate others.

Use this policy together with:

- `policies/release-readiness-policy.md` for release gates and evidence
- `policies/cross-repo-compatibility-policy.md` for dependency-order validation and linked PR expectations
- `policies/feature-status-and-graduation-policy.md` for unreleased vs released feature claims

## Why versions differ

Versions differ because different repositories own different promises:

1. `xrtm` owns the top-level product shell, newcomer path, and operator-facing release story.
2. support packages such as `data`, `forecast`, `eval`, and `train` own their own package APIs, schemas, and runtime contracts.
3. `xrtm.org` presents released truth but is not itself the runtime product version.
4. `governance` owns policy and schema language, not a single stack-wide runtime version number.

Different promises change at different rates. A support package may need a patch release without changing the top-level product story, while `xrtm` may need a product-anchor release because the released CLI, install flow, or default workflow changed even if some support packages did not.

## Ownership by repository

| Repository | What it owns | Versioning rule |
| --- | --- | --- |
| `governance` | shared policies, schemas, compatibility rules, release discipline | policy/schema versions are explicit where needed, but this repo does not define one forced shared runtime version for every repo |
| support packages (`data`, `forecast`, `eval`, `train`, similar libraries) | package APIs, serialized/runtime contracts, provider behavior, install metadata | version independently according to the package's own published surface and compatibility obligations |
| `xrtm` | product shell, top-level CLI, release-command contracts, install expectations, run-artifact expectations | owns the product-anchor version for "current XRTM release" |
| `xrtm.org` | released documentation, homepage/site claims, release presentation | mirrors released truth; site edits do not invent or redefine runtime package versions |

## `xrtm` is the product-anchor version

When maintainers, docs, or release notes say "XRTM `vX.Y.Z`", the anchor is the published `xrtm` package version.

Operational rules:

1. newcomer docs, operator quickstarts, release summaries, and homepage proof blocks should anchor to the released `xrtm` product surface
2. support package releases do not automatically redefine the "current XRTM release"
3. if a stack change alters the released top-level install path, CLI contract, default workflow, or user-consumed run artifacts, the authoritative release move is the `xrtm` release
4. `xrtm` must validate the intended released support-package set before the product release is treated as complete

## Support packages version independently

Support packages do not need to share version numbers with `xrtm` or with each other.

Operational rules:

1. bump a support package when its own released surface changes or when its own bugfix/security/compatibility release is warranted
2. do not bump a support package only to "match the train" numerically
3. a support package may release ahead of or behind `xrtm` if the published compatibility story remains honest
4. `xrtm` may consume a range of support-package versions, but release-pinned docs and site claims must describe only the versions and behaviors actually validated for the released product path
5. if `xrtm` depends on new support-package behavior, `xrtm` must update its dependency constraints, validation evidence, and release-safe contract/docs before the stack can claim that behavior as released

## Release trains are coordination labels, not forced shared versions

A release train is a coordination label for a set of changes moving together through validation and release planning. It is not a requirement that every repository publish the same `X.Y.Z`.

Every train record should identify:

1. the anchor `xrtm` version or candidate ref, if the train changes the product surface
2. the exact support-package versions, ranges, or candidate refs the train expects
3. which docs/contracts/site claims are supposed to move in that train
4. which items are deferred to a later train

Rules:

1. a repo may join, miss, or leave a train based on scope and readiness; do not hold unrelated package releases just to preserve numeric symmetry
2. train labels may be named after an `xrtm` anchor release, milestone, or release window, but the label is coordination metadata rather than a shared semantic version
3. merge and release decisions must use explicit versions/refs and validation evidence, not vague "same train" assumptions

## When packages, docs, contracts, and site claims must move together

When a released surface changes, all user-visible truth for that surface must move together in the same coordinated release move.

The minimum coordinated set is:

1. the released package artifact or dependency reference users actually install
2. the authoritative contract or compatibility record (`xrtm` release-command contract, schema version, or equivalent owning-repo contract)
3. release-pinned docs/examples that describe the changed surface
4. mirrored site/homepage claims that present the changed surface to newcomers
5. release validation evidence against the intended artifact set

Use this table for decisions:

| Change type | What must move together | What may wait |
| --- | --- | --- |
| support-package internal refactor with no stable-surface change | package release only, if any | `xrtm` docs/site/contract updates |
| support-package release that changes behavior `xrtm` exposes or requires | support-package release, `xrtm` dependency update, downstream validation, and any affected release-pinned docs/contracts/claims | unrelated repos not touched by the stable surface |
| top-level `xrtm` CLI/install/default-workflow change | `xrtm` release, release-command contract, release-pinned docs, mirrored site claims, released-stack smoke | advanced/next-release docs for later features |
| governance policy/schema change that alters public compatibility language | governance first, then owning implementation/docs updates that make the claim true, then site mirrors | downstream mirrors until source-of-truth repos are updated |
| docs/site-only correction of an already released fact | docs/site correction may land alone if it restores released truth | any unreleased feature/version promotion |

Hard rule: docs, contracts, and site pages must not advertise a changed released surface before the package artifacts and validation evidence exist.

## Concrete examples

- `forecast` ships a bugfix release with no change to the top-level `xrtm` product contract: release `forecast` independently; `xrtm` does not need a matching version bump just for symmetry.
- `forecast` adds behavior that changes the default `xrtm run` path: release the needed `forecast` version, update `xrtm` dependency and contract/docs, validate the stack, then publish the anchored `xrtm` release before the site presents that path as released.
- a docs page still pins an older package version after the released stack moved on: correct the docs/site claim to match the already released truth, but do not use a docs-only change to pre-announce an unpublished package or train.
