# Release Readiness Policy

This policy defines the minimum gates for coordinated XRTM releases. It complements the PR acceptance policy: PR review decides whether a change is worth merging; release readiness decides whether the merged stack is safe to publish.

## Supported runtime boundary

All released Python packages must declare only the Python versions that are validated by CI and release smoke tests.

Current supported range:

- Python `>=3.11,<3.13`

Python 3.13 is intentionally excluded until the dependency stack is validated there. If a future release expands support, the change must include CI coverage, clean installation checks, and a short compatibility note.

## Required release gates

Before publishing any package release:

1. The release branch or PR must pass repository CI.
2. Local package checks must install freshly built artifacts, not stale cached wheels.
3. A clean supported-Python environment must install the candidate release and run the package's CLI/import smoke.
4. Cross-package changes must be validated in dependency order.
5. Documentation must mention user-visible behavior changes, compatibility changes, and known unsupported environments.
6. Corpus-aware validation must pass using a Tier 1 release-gate-approved corpus with sufficient coverage (`xrtm validate run --release-gate-mode`).
7. Performance budgets must be met for the appropriate scenario (`xrtm perf run --fail-on-budget`).

Before publishing a coordinated stack release:

1. Lower-layer packages must be released and visible on the package index before dependent packages raise their minimum versions.
2. The top-level `xrtm` package must pass a stack compatibility smoke using the released package set.
3. Provider-free product smoke must pass.
4. The disposable Docker clean-room provider-free acceptance lane must pass from wheelhouse artifacts before publish, and must pass again from PyPI artifacts before the release record is considered complete.
5. Local LLM smoke is required when provider or product-shell behavior touches local model execution.
6. Local-LLM clean-room acceptance is additionally required for those local-model changes when a compatible runner/model setup is available; otherwise the release record must explicitly note why the local-LLM lane remains a manual or deferred follow-up.
7. Python versions outside the declared support range must not resolve the release.
8. Corpus-aware validation must pass on at least one Tier 1 corpus with `--release-gate-mode` and a minimum of 100 forecasts across 10 iterations.
9. Performance budgets must pass for `provider-free-smoke` scenario with default or stricter budgets.

## Recommended release order

1. `xrtm-data`
2. `xrtm-eval`
3. `xrtm-forecast`
4. `xrtm-train`
5. `xrtm`
6. documentation and site updates

## Tooling policy

Repository automation should prefer `uv` for Python dependency installation and virtual environment operations. Direct `pip` use is allowed only when a workflow is explicitly testing end-user `pip install` behavior or package-index resolution.

If a workflow uses direct `pip`, the step name or comment must make that purpose clear.

The workspace clean-room lane is:

- `./workspace.sh docker-provider-free-acceptance --artifact-source wheelhouse`
- `./workspace.sh docker-provider-free-acceptance --artifact-source pypi`
- `./workspace.sh docker-local-llm-acceptance --artifact-source wheelhouse`

The provider-free lane builds a disposable `docker run --rm` validation container, installs only from wheelhouse or PyPI artifacts, mounts the checkout read-only for release-pinned docs/examples, and persists logs plus run artifacts under `acceptance-studies/docker-provider-free/`.

The local-LLM acceptance lane uses Docker Compose to keep the acceptance runner disposable while a separate llama.cpp service container owns model state for the bounded real-model smoke. It reads model weights from `XRTM_LOCAL_LLM_MODEL_DIR`/`XRTM_LOCAL_LLM_MODEL` (or explicit CLI overrides) and persists logs plus run artifacts under `acceptance-studies/docker-local-llm/`.

Release-readiness evidence should record:

- the exact lane command or CI workflow run
- the artifact source (`wheelhouse` for pre-publish candidates, `pypi` for published verification)
- the persisted `summary.json` path or uploaded artifact bundle
- any local-LLM skip/defer note when provider/local-model behavior changed but the bounded lane could not run on available infrastructure

## Release-gated command claims

Top-level newcomer/operator docs must stay behind the published package surface.

- `xrtm/docs/release-command-contract.json` is the source of truth for release-safe command claims.
- README/getting-started/operator/site pages must pass the automated release-claim checks against that contract.
- Command-surface additions on `main` stay out of those pages until the matching package release is published, the contract version is updated, and released-stack smoke passes against that version.

## Release-pinned documentation policy

Treat these as release-pinned surfaces unless a repo explicitly labels them otherwise:

- README hero flows and install snippets
- getting-started, newcomer, and operator quickstarts
- homepage proof blocks and default workflow pages
- versioned API/CLI examples that claim current published behavior

Rules:

1. Release-pinned pages may describe only commands, APIs, versions, and behavior that already exist in published artifacts.
2. If a useful feature is real in source but not published yet, move the explanation to the owning repo's next-release track or clearly labeled advanced docs instead of mixing it into the default released path.
3. If a page would become misleading without an unreleased feature, split the page or defer the edit; do not "pre-announce" the feature inside release-pinned instructions.
4. Promotion into release-pinned docs requires the docs update, release contract update, published version/reference update, and released-artifact smoke evidence in the same coordinated release move.

## Feature graduation discipline

Use `policies/feature-status-and-graduation-policy.md` whenever a feature exists in source or branch docs but is not yet part of the published release surface.

Before a branch-only convenience can move into release-pinned docs or release command contracts:

1. The owning repo must record it as `next-release`, `advanced/experimental`, or `redesign-required` with explicit graduation criteria.
2. Release-pinned docs must stay on the currently published package surface until the package is actually published.
3. Promotion requires the contract/docs update and released-stack smoke in the same coordinated release move.
4. Features marked `redesign-required` must not be presented as imminent release candidates until the public contract is settled.

## Validation and performance evidence

Release candidates must include validation and performance evidence demonstrating regression-free behavior:

### Corpus-aware validation

Run the validation harness with release-gate mode:

```bash
xrtm validate run \
  --corpus-id xrtm-real-binary-v1 \
  --release-gate-mode \
  --provider mock \
  --limit 100 \
  --iterations 10 \
  --output-dir .cache/validation
```

The validation artifact must show:
- Tier 1 corpus usage (`release_gate_approved: true`)
- Successful completion of all iterations
- Forecast correctness (Brier scores within expected ranges)
- No schema validation errors

Approved Tier 1 corpora include `xrtm-real-binary-v1` (seed corpus) and `forecastbench` (preferred for comprehensive coverage). See `xrtm/docs/operator-runbook.md` for corpus tier classification.

### Performance budget compliance

Run the performance harness with budget enforcement:

```bash
xrtm perf run \
  --scenario provider-free-smoke \
  --iterations 5 \
  --limit 10 \
  --fail-on-budget \
  --output performance.json
```

The performance artifact must show:
- Mean iteration duration within default or stricter budgets
- P95 iteration duration within default or stricter budgets
- Budget status `passed` or better

Default budgets:
- `provider-free-smoke` (limit=10): mean ≤50ms, p95 ≤100ms
- `provider-free-scale` (limit=100): mean ≤500ms, p95 ≤1000ms

Record validation and performance artifacts with release notes or attach to release PRs for evidence traceability.

## Release blocker examples

Do not publish if any of these are true:

- CI is red or pending on the release branch.
- Built-artifact installation fails in a clean supported-Python environment.
- A dependent package version is not yet visible on the package index.
- A release resolves on an unsupported Python version.
- Product smoke fails in provider-free mode.
- The disposable Docker clean-room provider-free acceptance lane fails.
- Local LLM smoke fails after bounded retry when the change affects provider/local-model behavior.
- The disposable Docker clean-room local-LLM acceptance lane fails after bounded retry, or the release record omits the required skip/defer note.
- Documentation claims support for versions, commands, or provider behavior that is not validated.
- Corpus-aware validation fails or uses a non-release-gate-approved corpus (Tier 2/3).
- Performance budgets are exceeded for the corresponding scenario.
- Validation or performance evidence is missing or incomplete.
