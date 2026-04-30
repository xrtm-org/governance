# PR Acceptance Policy

This policy is the shared decision record for reviewing pull requests across the XRTM organization. Treat open PRs as evidence and candidate implementations, not as changes to merge automatically.

## Decision categories

Use one decision for each PR or PR family.

| Decision | Use when |
| --- | --- |
| Accept as-is | The PR is current, non-overlapping, tested, compatible, and already matches repository conventions. This should be rare. |
| Accept with changes | The idea is valuable, but the PR needs fixes for API safety, edge cases, tests, performance, or maintainability before merge. |
| Supersede | Multiple PRs overlap, the PR is stale, or a consolidated local implementation is safer than merging the original branch. |
| Reject or close | The PR is duplicate, regressive, risky, too narrow, breaks public APIs without migration, or adds maintenance cost without clear value. |
| Defer | The idea is valid but not release-blocking, needs a separate design, or depends on future schema/provider work. |

## Acceptance criteria

A PR can be accepted only when it is:

1. Correct: covered by tests, handles edge cases, and does not hide or swallow errors.
2. Compatible: preserves public APIs and schemas, or includes an explicit migration path and compatibility tests.
3. Measurable: improves correctness, robustness, performance, or release readiness. Neutral micro-optimizations are not enough.
4. Maintainable: follows repository patterns, reuses helpers, avoids duplicated logic, and avoids brittle special cases.
5. Validated: passes local focused tests, package-level checks, relevant smoke/stress lanes, and GitHub CI.

## Review procedure

1. Group overlapping PRs into a single PR family before deciding.
2. Read the diff, tests, issue/PR discussion, and base branch.
3. Check whether the PR is current, stacked on another PR, or already superseded locally.
4. Compare the implementation against existing repository patterns and XRTM layer boundaries.
5. Run focused tests or reproduce the claimed improvement locally when feasible.
6. Record the decision and evidence in the PR disposition tracker.
7. Prefer a consolidated replacement over merging several overlapping partial fixes.

## Validation gates

Every accepted or superseding PR must pass its package gate.

### Python packages

- `uv run ruff check .`
- `uv run mypy .` or the repository's configured mypy target.
- `uv run pytest tests` for `data`, `eval`, and `train`.
- `uv run pytest tests/unit` plus relevant integration or local-skipped tests for `forecast`.

### Cross-repo gates

Before release-candidate approval, run the workspace validation matrix:

- `./workspace.sh check-python`
- `./workspace.sh deps-audit`
- `./workspace.sh schema-audit`
- `./workspace.sh stress-fast`
- `./workspace.sh real-e2e`
- `./workspace.sh real-e2e-eval-train`
- `./workspace.sh bench-real --limit 2 --iterations 2`
- `./workspace.sh package-check`
- `./workspace.sh check-site`

Local GPU gates are manual but required before release:

- `./workspace.sh local-llm-start`
- `./workspace.sh check-local-llm`
- `./workspace.sh check-offline-e2e`
- `./workspace.sh real-e2e-local-llm`
- `./workspace.sh bench-real --provider local-llm --limit 2 --iterations 1`
- `./workspace.sh stress-local-llm`
- `./workspace.sh local-llm-stop`

## Release blockers

Do not release if any of these are true:

- Lint, type checks, unit tests, or relevant integration tests fail.
- GitHub CI is red on a release branch or release PR.
- `package-check` fails from clean built artifacts.
- Provider-free real-question E2E or eval/train real E2E fails.
- Local llama.cpp/Qwen real E2E fails after bounded retry handling.
- `xrtm.org` has high or critical npm audit findings.
- Public schema/API changes are undocumented or lack compatibility tests.
- Dirty or unreviewed local changes are included in release artifacts.

## Merge and release order

Merge focused PRs in dependency order:

1. `governance`
2. `data`
3. `eval`
4. `forecast`
5. `train`
6. `xrtm`
7. root workspace helper changes, if separate
8. `xrtm.org`

Release packages in dependency order:

1. `xrtm-data`
2. `xrtm-eval`
3. `xrtm-forecast`
4. `xrtm-train`
5. `xrtm`
6. `xrtm.org` documentation/site deployment

## Non-blocking tracked items

These should remain visible but do not block release by themselves:

- Moderate-only `xrtm.org` audit findings in upstream Docusaurus development-server chains, as long as high and critical findings remain zero.
- Larger live-source integrations beyond the deterministic offline real-question corpus.
- Broader schema canonicalization beyond compatibility shims.
- Low-value or risky micro-optimization PRs that lack clear benchmark or correctness value.
