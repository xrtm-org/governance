# Feature Status and Graduation Policy

This policy keeps useful branch-only features from living in limbo. It defines how XRTM labels unreleased-but-desired work, where that work is documented, and what must happen before it graduates into release-pinned docs or published package claims.

For release publication gates, use this policy together with `policies/release-readiness-policy.md`.

## Status labels

Every user-facing feature or convenience must have exactly one current status:

| Status | Meaning | Allowed surfaces |
| --- | --- | --- |
| `released` | Published in the current package/site release and validated against installed artifacts. | Release-pinned docs, README hero flows, homepage proof blocks, and release command contracts. |
| `next-release` | Valuable, already real in source or coordinated docs drafts, and a reasonable candidate for the next coordinated release once gates pass. | Owning repo next-release track, dedicated next-release site/docs pages, contributor guidance, and roadmap-adjacent planning. |
| `advanced/experimental` | Real or partially real, but still too specialized, governance-heavy, or proof-thin for the default shipped path. | Advanced docs, examples, roadmap, and contributor guidance with explicit labeling. |
| `redesign-required` | The current implementation or naming is not yet the contract we should publish. | Internal planning, next-release track, and contributor guidance. Keep out of release-pinned docs and hero claims. |

## Required records for unreleased work

A feature may not remain branch-only without an explicit record.

For every `next-release`, `advanced/experimental`, or `redesign-required` item, the owning repo must record:

1. feature name or command family
2. owning repo and audience
3. current status label
4. why that label is correct right now
5. the exact evidence needed to promote it, keep it advanced, or redesign it

For top-level `xrtm` CLI conveniences, keep that record in `xrtm/docs/next-release-feature-track.md`. Public-facing summaries may mirror it on `xrtm.org`, but the owning repo remains authoritative for command-level details.

## Release boundary rules

1. Release-pinned docs must describe only `released` behavior.
2. `next-release`, `advanced/experimental`, and `redesign-required` items must be clearly labeled where they appear.
3. Branch-only commands must not be introduced into `README.md`, getting-started pages, operator runbooks, homepage proof sections, or release command contracts until the matching package release is published.
4. If a feature exists in source but is intentionally unreleased, point readers to the next-release track instead of smuggling it into release-pinned walkthroughs.
5. If a feature's semantics are still unsettled, mark it `redesign-required` instead of leaving it implied, hidden, or half-promised.

## Graduation checklist

Before a `next-release` item becomes `released`, the owning repo must complete all of the following:

1. Validate the feature against freshly built or freshly installed release artifacts on supported runtimes.
2. Run the repo's normal lint/type/test/build gates plus any feature-specific smoke or acceptance commands.
3. Update release-pinned docs only in the same change set that updates the published package version or release contract.
4. Update `xrtm/docs/release-command-contract.json` (or the equivalent release-safe contract) when top-level command claims change.
5. Record the status move in the owning repo's next-release track and remove or downgrade stale roadmap wording if needed.

## Advanced and redesign paths

Not every useful branch feature should graduate immediately.

- Keep a feature `advanced/experimental` when it depends on optional infrastructure, release-engineering-only workflows, special data/corpus governance, or user sophistication beyond the honest default path.
- Mark a feature `redesign-required` when the implementation works technically but the public contract, UX naming, privacy story, or packaging story is still wrong.
- Reassess these items during release planning; do not let them drift without an explicit status update.

## Cross-repo coordination

If a feature changes schemas, packaging boundaries, dataset policy, or public workflow promises across repositories:

1. land governance policy or schema changes first
2. update implementation repos next
3. update `xrtm.org` last so the public explanation mirrors accepted source-of-truth decisions
