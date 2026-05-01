# xrtm Governance

**Current Status:** Phase 1 (Foundation)

This repository serves as the central source of truth for the **xrtm** organization. It contains the core philosophy, architectural standards, and data schemas that all xrtm tools must adhere to.

## Purpose
We separate our "Standards" from our "Implementation" to ensure consistency across the ecosystem.
* **Philosophy:** To understand the "Why" behind our focus on forecasting and zero leakage, read [MISSION.md](MISSION.md).
* **Technical Standards:** To understand the data structures required for interoperability, see the [schemas/](schemas/) directory.
* **PR Acceptance:** To decide whether to accept, modify, supersede, reject, or defer pull requests, use [policies/pr-acceptance-policy.md](policies/pr-acceptance-policy.md).

## Core Standards

### 1. The Forecast Object
All inference engines and evaluation tools must exchange data using the **Forecast Object Standard**.
* **Current Version:** v1.1
* **Definition:** [schemas/forecast_object_v1.1.json](schemas/forecast_object_v1.1.json)
* **Previous Version:** [schemas/forecast_object_v1.json](schemas/forecast_object_v1.json)
* **Compatibility Policy:** [schemas/compatibility-policy.md](schemas/compatibility-policy.md)
* **Key Features:** Enforces strict fields for `snapshot_time` (Zero Leakage) and `reasoning_trace` (Causal Graphs). v1.1 adds optional parametric `distribution` support (Beta, Gaussian Bounded) for epistemic uncertainty; deprecated `confidence_interval` remains compatible.

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

## Triage and Review Process
To ensure consistent and reproducible decisions for PRs and issues:
* **Before Reviewing:** Read the [Triage Matrix](policies/triage-matrix.md) to classify PRs and issues by scope, priority, risk, and compatibility impact.
* **During Review:** Apply the decision criteria from [PR Acceptance Policy](policies/pr-acceptance-policy.md).
* **After Decision:** Record the disposition, rationale, and evidence in [PR Disposition Log](policies/pr-disposition-log.md).
* **Communication:** Use triage labels (`disposition:*`, `priority:*`, `scope:*`, `type:*`) and add brief comments to PRs/issues explaining next steps.

The triage process makes implicit knowledge explicit, enabling maintainers to track patterns, avoid redundant discussions, and provide clear feedback to contributors.
