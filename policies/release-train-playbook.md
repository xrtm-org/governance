# Release Train Playbook

This playbook turns coordinated multi-repo work into an explicit, repeatable operating path.

Use it together with:

- `policies/cross-repo-compatibility-policy.md`
- `policies/pr-acceptance-policy.md`
- `policies/release-readiness-policy.md`

The goal is simple: no hidden branch conventions, no silent sibling fallback, and no ambiguous release order.

## When to start a release train

Start a coordinated release train when a change:

1. touches a documented schema, API, CLI contract, run artifact, or packaging/version floor consumed by another repo;
2. changes cross-repo CI or compatibility validation behavior; or
3. requires docs or site updates to land with product or governance changes.

If the change is internal-only and does not affect a stable cross-repo surface, normal single-repo flow is fine.

## Required artifacts

Every coordinated train needs:

1. **One coordination record**: an issue or lead PR that links the PR family.
2. **Explicit refs**: branches, tags, commit SHAs, or PR refs for each upstream dependency under test.
3. **Validation evidence**: workflow runs, local checks, or release-gate artifacts tied to those exact refs.
4. **A dependency-order plan**: which repo merges first, which repo validates next, and what post-merge checks remain.

## Dependency order

Use dependency order unless the change is documentation-only in a downstream repo:

1. `governance`
2. `data`
3. `eval`
4. `forecast`
5. `train`
6. `xrtm`
7. `xrtm.org`

Skip repositories that are not affected, but never invert the order for affected contract surfaces.

## Coordination checklist

### 1. Open the coordination record

Record:

- why the train exists;
- the stable surface being changed;
- affected repositories;
- merge order;
- release order, if publication is expected; and
- the owner for final post-merge validation.

Use a table like this in the issue or lead PR:

| Repo | Change owner | Exact upstream ref(s) under test | Validation evidence | Merge status |
| --- | --- | --- | --- | --- |
| governance | @owner | n/a | PR / CI link | open |
| data | @owner | governance@`<sha-or-tag>` | PR / CI link | pending |
| forecast | @owner | data@`<ref>`, eval@`<ref>` | PR / CI link | pending |
| xrtm | @owner | data@`<ref>`, eval@`<ref>`, forecast@`<ref>`, train@`<ref>` | PR / CI link | pending |

### 2. Open linked PRs

Each PR in the family should say:

- which coordination record it belongs to;
- which upstream refs or releases it expects;
- whether it blocks release publication; and
- what downstream validation must happen after merge.

Do not rely on “same branch name exists in sibling repo” as the coordination mechanism.

### 3. Run the correct validation lane

#### Default lane

Normal `push` and `pull_request` CI should validate against explicit default upstream refs, usually `main` or the normal released dependency range.

Use this lane when:

- the PR is not coordinating unpublished upstream work; or
- you need the standard baseline signal for an otherwise coordinated change.

#### Coordinated lane

When unpublished upstream changes are involved, run CI with explicit refs and record them in the coordination record.

Current workflow inputs:

- `forecast/.github/workflows/ci.yml`
  - `data_ref`
  - `eval_ref`
  - `coordination_context`
- `xrtm/.github/workflows/ci.yml`
  - `data_ref`
  - `eval_ref`
  - `forecast_ref`
  - `train_ref`
  - `coordination_context`

Use branch names, tags, commit SHAs, or PR refs such as `refs/pull/123/head`. Record both the requested ref and the workflow run URL.

### 4. Merge in dependency order

After an upstream PR merges:

1. update downstream PR descriptions from temporary branch refs to the merged commit or release candidate;
2. rerun downstream coordinated validation against that exact merged ref; and
3. remove any obsolete temporary alias or placeholder note.

### 5. Run post-merge validation before declaring the train done

Minimum expectations:

- downstream CI has been rerun against merged upstream refs;
- release notes or user-facing docs have been updated where needed;
- `xrtm` still passes product-shell compatibility validation for the intended stack; and
- any temporary coordination note in PRs is replaced with the final merged refs or published versions.

For release-candidate or publication work, also run the gates required by `policies/release-readiness-policy.md`.

## Publication checklist

Before publishing a coordinated stack release:

1. publish lower-layer packages before dependent packages raise minimum versions;
2. wait until each upstream package is visible to consumers;
3. validate `xrtm` against the exact published package set;
4. update `xrtm.org` only after published behavior is real and documented; and
5. attach validation/performance evidence to the release PR or release notes.

## Anti-patterns to avoid

Do not:

- use same-name sibling branches as the default compatibility signal;
- depend on hidden branch aliases for merge or release decisions;
- merge downstream minimum-version bumps before upstream artifacts are available;
- treat green upstream CI as sufficient proof for downstream compatibility; or
- leave post-merge validation implicit or unowned.
