# xrtm Governance

**Current Status:** Phase 1 (Foundation) · Zero-backlog baseline recorded (2026-05-01)

This repository serves as the central source of truth for the **xrtm** organization. It contains the core philosophy, architectural standards, and data schemas that all xrtm tools must adhere to.

## Purpose
We separate our "Standards" from our "Implementation" to ensure consistency across the ecosystem.
* **Philosophy:** To understand the "Why" behind our focus on forecasting and zero leakage, read [MISSION.md](MISSION.md).
* **Technical Standards:** To understand the data structures required for interoperability, see the [schemas/](schemas/) directory.
* **PR Acceptance:** To decide whether to accept, modify, supersede, reject, or defer pull requests, use [policies/pr-acceptance-policy.md](policies/pr-acceptance-policy.md).
* **Release Readiness:** For release publication gates including corpus-aware validation and performance budgets, see [policies/release-readiness-policy.md](policies/release-readiness-policy.md).
* **Stack Versioning:** For why package versions differ, what `xrtm` anchors, what release trains mean, and when package/docs/contracts/site updates must move together, see [policies/stack-versioning-policy.md](policies/stack-versioning-policy.md).
* **Cross-Repo Compatibility:** For stable-surface changes, linked PR families, downstream validation, and published-surface coordination, see [policies/cross-repo-compatibility-policy.md](policies/cross-repo-compatibility-policy.md).
* **Feature Status & Graduation:** For released vs next-release vs advanced vs redesign-required labeling, see [policies/feature-status-and-graduation-policy.md](policies/feature-status-and-graduation-policy.md).
* **Interface Parity & Claims:** For when CLI/WebUI/TUI/API capabilities can be called parity-ready, CLI-only, WebUI-only, advanced, or redesign-required, see [policies/interface-parity-and-claim-ownership-policy.md](policies/interface-parity-and-claim-ownership-policy.md).
* **Product Story & Structure:** For canonical rerun rules, macro-reorg triggers, and the XRTM story hierarchy, see [policies/product-story-and-architecture-guardrails.md](policies/product-story-and-architecture-guardrails.md).

## Core Standards

### 1. The Forecast Object
All inference engines and evaluation tools must exchange data using the **Forecast Object Standard**.
* **Current Version:** v1.1
* **Definition:** [schemas/forecast_object_v1.1.json](schemas/forecast_object_v1.1.json)
* **Previous Version:** [schemas/forecast_object_v1.json](schemas/forecast_object_v1.json)
* **Compatibility Policy:** [schemas/compatibility-policy.md](schemas/compatibility-policy.md)
* **Key Features:** Establishes the shared forecast request / forecast result vocabulary, enforces strict `snapshot_time` and `reasoning_trace` requirements, and reserves compatibility guidance for legacy aliases such as `ForecastQuestion`, `ForecastOutput`, `question_id`, `structural_trace`, and `reporting_lane`. v1.1 adds optional parametric `distribution` support (Beta, Gaussian Bounded) for epistemic uncertainty; deprecated `confidence_interval` remains compatible.

## The Ecosystem
This governance repository defines the standards for the following software components:

| Repository | Role | Description |
| :--- | :--- | :--- |
| **[xrtm-forecast](https://github.com/xrtm-org/forecast)** | Inference | The runtime engine for generating predictions. |
| **[xrtm-data](https://github.com/xrtm-org/data)** | Context | Tools for snapshotting history and preventing data leakage. |
| **[xrtm-eval](https://github.com/xrtm-org/eval)** | Verification | The scoring system for probabilistic integrity and resolution. |
| **[xrtm-train](https://github.com/xrtm-org/train)** | Evolution | Training frameworks optimized for forecasting accuracy. |

## Usage for Contributors
When building a new tool or agent for xrtm:
1. **Read the Mission:** Ensure your feature aligns with the goal of "Forecasting as Intelligence."
2. **Validate Outputs:** Ensure your code produces JSON that validates against the schemas in this repo.
3. **Propose Changes:** To change a standard (e.g., adding a field to the Forecast Object), submit a Pull Request to this repository first.
4. **Review PRs Carefully:** Do not merge every open PR. Apply the [PR Acceptance Policy](policies/pr-acceptance-policy.md) and record whether a PR is accepted as-is, accepted with changes, superseded, rejected, or deferred.

For the GitHub-first contributor flow, start with [CONTRIBUTING.md](CONTRIBUTING.md). It summarizes local validation, repo-role boundaries, and when downstream repos need coordinated follow-up.

## Maintainer quick rules

1. Keep release-pinned docs and quickstarts on the currently published package surface only. Branch-only value belongs in next-release or advanced docs with explicit labels.
2. Give every unreleased feature an explicit status, target release train or review point, and concrete graduation evidence in the owning repo.
3. Treat documented APIs, schemas, CLI commands, run artifacts, install/version expectations, and release-pinned docs as stable published surfaces unless governance says otherwise.
4. Merge only after repo-local gates pass; release only after the release-readiness gates and released-artifact smoke pass with recorded evidence.
5. Treat the published `xrtm` version as the product anchor. Support packages may version independently; release trains coordinate validated version sets rather than forcing shared version numbers.
6. Claim CLI/WebUI parity only when the owning repo's parity matrix marks the capability `parity-ready` and the required evidence exists.

## Triage and Review Process
To ensure consistent and reproducible decisions for PRs and issues:
* **Before Reviewing:** Read the [Triage Matrix](policies/triage-matrix.md) to classify PRs and issues by scope, priority, risk, and compatibility impact.
* **During Review:** Apply the decision criteria from [PR Acceptance Policy](policies/pr-acceptance-policy.md).
* **After Decision:** Record the disposition, rationale, and evidence in [PR Disposition Log](policies/pr-disposition-log.md).
* **Communication:** Use triage labels (`disposition:*`, `priority:*`, `scope:*`, `type:*`) and add brief comments to PRs/issues explaining next steps.

The triage process makes implicit knowledge explicit, enabling maintainers to track patterns, avoid redundant discussions, and provide clear feedback to contributors.
