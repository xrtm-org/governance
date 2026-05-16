# Cross-Repository Compatibility and Coordination Policy

This policy defines how XRTM manages compatibility while the implementation remains split across `data`, `forecast`, `xrtm`, and `xrtm.org`.

The repository split remains in place for now. Coordination must therefore happen through explicit contracts, linked pull requests, and explicit validation evidence rather than same-branch assumptions or ad hoc branch aliases.

Use this policy together with:

- `policies/pr-acceptance-policy.md` for merge decisions
- `policies/stack-versioning-policy.md` for anchor-version ownership, release-train meaning, and docs/contract coordination rules
- `policies/release-readiness-policy.md` for release publication gates

## Stable contract surfaces vs. internal surfaces

Treat the following surfaces as stable unless a versioned change or documented migration plan says otherwise.

| Repository | Stable contract surface | Internal surface |
| --- | --- | --- |
| `data` | Documented package APIs, serialized schema/data payloads, snapshot semantics, and compatibility behavior consumed by downstream repos | Private modules, provider internals, test fixtures, and local-only implementation details |
| `forecast` | Documented package APIs, provider-facing integration contracts, forecast/runtime behavior consumed by `xrtm`, and compatibility shims documented for callers | Internal orchestration details, experimental examples, test helpers, and private provider plumbing |
| `xrtm` | Documented CLI commands, documented Python entrypoints, run-artifact contracts, and supported install/version expectations for the product shell | Internal workflow wiring, local caches, temporary scaffolding, and non-documented implementation details |
| `xrtm.org` | Published documentation pages and release notes as a presentation of released behavior | Theme/components, build tooling, navigation implementation, and editorial workflow internals |

Rules:

1. Breaking a stable surface requires a versioned contract change or an explicit migration plan.
2. Internal-only refactors can ship independently if they do not change a stable surface.
3. If maintainers disagree about whether a surface is stable, treat it as stable until governance or repository docs say otherwise.

## Published-surface change management

These changes need extra discipline even when they look "small":

- install snippets, version floors, and dependency expectations
- documented CLI or API examples meant for the current released path
- README hero flows, getting-started pages, operator runbooks, and homepage proof blocks
- run-artifact shapes, exported file semantics, and other user-consumed output contracts

When a change touches one of those surfaces:

1. Name the exact owning repo and stable surface in the PR or coordination record.
2. Decide explicitly whether the change is `released` now or still `next-release` / `advanced/experimental` / `redesign-required`.
3. Land the authoritative source-of-truth update first (`governance` or the owning product/package repo), then mirror it downstream.
4. Record the exact downstream validation needed for the next consumer in the chain, especially `forecast -> xrtm` and `xrtm -> xrtm.org`.
5. Keep the default released docs on the already-published behavior until the corresponding package and contract move is real.

## Dependency expectations in practice

For the current core-repo coordination path, the dependency chain is:

```text
data -> forecast -> xrtm -> xrtm.org
```

In practice, this means:

- `data` is an upstream contract repo. Changes to exported schemas, serialized fields, snapshot behavior, or packaging can affect every downstream layer.
- `forecast` depends on compatible `data` contracts and becomes an upstream contract for `xrtm`.
- `xrtm` is the downstream product integrator. It must prove that the released or candidate package set works together before release.
- `xrtm.org` depends on governance and released product behavior for documentation truth. It is downstream of product and policy, not upstream of either.

The same coordination rules apply to other XRTM repos when they participate in the same contract chain.

## When coordinated pull requests are required

Create a linked PR family when a change does any of the following:

1. Changes a documented schema, serialized field, public API, CLI contract, or run artifact consumed by another repo.
2. Changes dependency version floors, install behavior, or packaging assumptions relied on by another repo.
3. Changes CI or automation behavior that resolves sibling repositories or cross-repo candidate artifacts.
4. Changes documentation or site content that must land with a product or governance change to stay accurate.

Coordinated PR expectations:

- One PR or issue must act as the coordination record and link all related PRs.
- Each affected PR must say which upstream ref, release candidate, or published version it expects.
- Merge order must follow dependency order unless the change is documentation-only in a downstream repo.
- Downstream PRs may remain open while upstream work is in flight, but they must not silently assume unpublished compatibility.

## When releases must be synchronized or blocked

Independent releases are acceptable only for internal-only changes that do not affect a stable contract surface.

Block release publication when a stable cross-repo surface changed and any of the following is still missing:

1. The upstream contract change is merged or a candidate artifact/ref is available.
2. The immediate downstream repo has validated against that exact candidate.
3. `xrtm` downstream smoke or integration validation is still pending for a change that can reach the product shell.
4. User-facing docs or site content still describe pre-change behavior without an explicit unreleased label.

Release sequencing for coordinated changes should be:

1. `governance` when policy or contract text changes
2. `data`
3. `forecast`
4. `xrtm`
5. `xrtm.org`

Downstream repos must not raise their minimum required upstream version until the upstream release is actually available to consumers.

## CI expectations for cross-repo compatibility

Default repository CI should validate against the normal supported dependency set, usually the latest released upstream version range.

When a change needs cross-repo validation:

1. Use explicit refs only: published pre-releases, commit SHAs, PR artifacts, or workflow inputs that name the tested upstream ref.
2. Record the exact upstream ref or artifact in the PR description, workflow input, or job summary.
3. Add downstream validation whenever the change can affect downstream install, runtime, CLI, schema, or artifact behavior.
4. Treat green upstream CI as necessary but not sufficient when a downstream contract is involved.

CI may use workspace-based validation during development, but merge and release decisions must be based on explicit, reproducible refs.

## Same-branch assumptions and branch aliases

Same-name branches across repos are a convenience for humans, not a compatibility contract.

Policy:

- Do not design CI around "current branch name exists in the sibling repo".
- Do not require hidden branch aliases as the normal way to prove compatibility.
- If a temporary branch alias is unavoidable before a better explicit-ref mechanism exists, it must be:
  - documented in every affected PR,
  - limited to short-lived coordination work,
  - replaced by an explicit ref or merged upstream change before release, and
  - removed once the coordinated PR family is complete.

No release decision may rely solely on a same-branch assumption or undocumented alias branch.

## Site and documentation authority

Authority order for cross-repo truth is:

1. `governance` for shared policies, versioned compatibility rules, and canonical contract language
2. Product/package repos for actual implementation behavior, release notes, and supported commands/APIs
3. `xrtm.org` for presentation, navigation, and discoverability

Implications:

- `xrtm.org` must link back to governance or product docs for contract claims.
- The site must not become the only place where compatibility rules exist.
- If site content disagrees with governance or the product repos, governance/product truth wins and the site must be corrected.
- Product and governance repos should carry the authoritative documentation needed for contributors and agents to coordinate work safely.
