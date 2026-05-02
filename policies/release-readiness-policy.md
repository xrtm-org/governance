# Release Readiness Policy

This policy defines the minimum gates for coordinated XRTM releases. It complements the PR acceptance policy: PR review decides whether a change is worth merging; release readiness decides whether the merged stack is safe to publish.

For the explicit operating sequence for linked PRs, dependency-order merges, workflow inputs, and post-merge validation, use `policies/release-train-playbook.md` together with this policy.

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

Before publishing a coordinated stack release:

1. Lower-layer packages must be released and visible on the package index before dependent packages raise their minimum versions.
2. The top-level `xrtm` package must pass a stack compatibility smoke using the released package set.
3. Provider-free product smoke must pass.
4. Local LLM smoke is required when provider or product-shell behavior touches local model execution.
5. Python versions outside the declared support range must not resolve the release.

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

## Release blocker examples

Do not publish if any of these are true:

- CI is red or pending on the release branch.
- Built-artifact installation fails in a clean supported-Python environment.
- A dependent package version is not yet visible on the package index.
- A release resolves on an unsupported Python version.
- Product smoke fails in provider-free mode.
- Local LLM smoke fails after bounded retry when the change affects provider/local-model behavior.
- Documentation claims support for versions, commands, or provider behavior that is not validated.
