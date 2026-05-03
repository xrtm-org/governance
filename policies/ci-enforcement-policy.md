# CI Enforcement Policy

## Purpose

Ensure all pull requests pass required CI checks before merge, and maintain consistency across the XRTM multi-repo system.

## Core Rule

**No PR merge without green CI.** Every open PR must pass its repository's required checks. Exceptions require explicit escalation.

## Required CI per Repository

### Core Packages

- **xrtm-data**, **xrtm-eval**, **xrtm-forecast**, **xrtm-train**: `ruff`, `mypy`, `pytest`
- **xrtm**: `ruff`, `mypy`, `pytest`, smoke tests
- **governance**: `ruff`, schema validation
- **xrtm.org**: `npm ci`, `npm run typecheck`, `npm run audit:policy`, `npm run build`

### Branch Protection

All core repos should have branch protection on `main` requiring:
- All status checks must pass
- PR review policy (maintainer discretion: may require reviews or allow auto-merge)

## Cross-Repo Dependencies and Merge Ordering

Some changes require coordinated merges across repositories. The current coordinated PR set should merge in this order:

1. **xrtm-org/data#29** — adds corpus registry and new splits/importer exports
2. **xrtm-org/forecast#27** — uses data surfaces; tests depend on data changes
3. **xrtm-org/xrtm#12** — imports new forecasting internals; depends on both data and forecast
4. **xrtm-org/xrtm.org#3** — site docs; depends on xrtm release-command-contract
5. **xrtm-org/governance#7** — policy updates; should merge after the above

### Rule: Sequential vs Parallel Coordination

- **Sequential coordination** (required): When PR A imports symbols introduced in PR B, PR B must be merged first, then PR A's CI will pass when it checks out B from main.
- **Parallel coordination** (optional): When repos share a branch (e.g., `copilot/xrtm-onboarding-stress`), they can develop together and merge in dependency order.

## CI Coverage

Each repository should have CI workflows that:

1. **Run on `pull_request` to `main`** — validate PRs before merge
2. **Run on push to `main`** — catch any post-merge issues
3. **Document required vs optional checks** — e.g., local GPU tests are optional; lint/type/tests are required
4. **Fail clearly** — error messages should point to remediation steps

## When CI Fails

1. **Code bug**: Fix the code and push to the PR branch; GitHub will re-run CI.
2. **CI environment issue**: Document the issue, investigate, and update CI if needed.
3. **Cross-repo dependency issue**: Ensure dependent repos are merged first, then re-trigger CI.
4. **Flaky test**: Investigate, fix, add retry logic if appropriate, or mark known-flaky with clear skip reason.

## Exceptions and Escalation

### Emergency Merge Without Green CI

In urgent situations (e.g., security hotfix), a maintainer may merge with red CI only if:

1. The issue is documented in the PR as a known exception
2. A linked issue exists tracking the CI remediation
3. The merge is followed by immediate investigation and fix
4. The exception is logged in the release notes

### Example Exception Pattern

```
Emergency merge of #XYZ due to [reason].
Known CI failure: [description of failure].
Tracked in #ABC for remediation.
```

## Release Gate

Before cutting any release, verify:

1. All open PRs for that package have merged with green CI
2. Post-merge main CI is green
3. Package build/install smoke passes from clean artifacts
4. Cross-repo compatibility has been verified (if multi-repo release)

## Future Review Triggers

Reassess this policy if:

- More than 2 sequential PRs are regularly required to land a feature (sign: architecture friction)
- CI regularly takes >15 min per repository (sign: CI bloat or environment issue)
- Unrelated PRs fail due to cross-repo pollution (sign: boundary leakage)

---

**Policy Version**: 1.0  
**Date**: May 2026  
**Approved By**: Architecture Review Group
