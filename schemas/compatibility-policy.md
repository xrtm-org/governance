# Schema Compatibility and Migration Policy

This policy governs changes to the Forecast Object contracts in this directory and their runtime counterparts in the xrtm packages.

## Contract Surfaces

| Area | Canonical contract | Accepted aliases or shims | Migration rule |
| --- | --- | --- | --- |
| Forecast request / result naming | Runtime `ForecastRequest` / `ForecastResult`; governance Forecast Object still uses `question` / `prediction` in v1.x. | Runtime keeps `ForecastQuestion` / `ForecastOutput` as compatibility aliases. | Use `ForecastRequest` / `ForecastResult` in new runtime docs and serialized examples. Governance object member names stay versioned until a new schema revision changes them explicitly. |
| Forecast request identifier | Runtime `forecast_request_id` on result and resolution objects. | Runtime still accepts `question_id` as an input alias and compatibility property. | New code must write `forecast_request_id`. Keep `question_id` parsing compatibility until a major-version removal window is announced. |
| Forecast probability | `prediction.probability` in governance; `ForecastOutput.probability` in runtime. | Runtime still accepts `confidence` as an input alias for `probability`. | New code must write `probability`. Keep `confidence` input compatibility until a major-version removal window is announced. |
| Reasoning trace | `prediction.reasoning_trace.narrative` and `prediction.reasoning_trace.causal_graph.{nodes,edges}`. | Runtime still accepts `reasoning`, `logical_trace`, and `logical_edges` as compatibility inputs and legacy mirrored properties; `forecast_path` is an allowed descriptive alias for the ordered node sequence. | New schema examples must use `reasoning_trace`. Runtime package examples may mention legacy field names only when documenting compatibility behavior. |
| Execution trace | Runtime `execution_trace` for ordered workflow-stage output. | Runtime still accepts `structural_trace` as an input alias and compatibility property. Governance Forecast Object v1.x does not yet standardize this field. | New runtime artifacts and examples must write `execution_trace`. Treat `structural_trace` as deprecated compatibility-only vocabulary. |
| Evaluation path | Eval/train public benchmark artifacts use `evaluation_path` for labeled reporting routes. | `reporting_lane` remains an accepted compatibility alias while v1.x artifacts are supported. | New scorecard and benchmark examples must write `evaluation_path`. Keep `reporting_lane` readable for existing consumers until a major-version removal window is announced. |
| Intervals | `prediction.distribution.credible_interval` when a parametric `distribution` is present. | `prediction.confidence_interval` and runtime `confidence_interval` remain deprecated compatibility fields. | New distribution-aware producers must write `credible_interval`. Consumers must continue to read `confidence_interval` while v1.x remains supported. |
| Distribution | `prediction.distribution` with `family`, Beta `alpha`/`beta`, or bounded-family parameters. | `BetaPrior.to_distribution_dict()` already emits a governance-compatible Beta distribution payload. `ForecastOutput` does not yet carry a `distribution` field. | Do not require `ForecastOutput.distribution` in v1.x compatibility tests. Broader runtime adoption needs a coordinated schema and package release. |
| Snapshot time | `metadata.snapshot_time`. | Runtime `MetadataBase.snapshot_time`. | Required for zero-leakage. Do not add alternate timestamp names to the governance object. |
| Resolution criteria | `question.resolution_criteria`. | Runtime `ForecastQuestion.resolution_criteria`. | Keep on the question object. Do not move criteria into evaluation result or resolution objects. |
| Ground truth / resolution | Evaluation-owned `ForecastResolution(forecast_request_id, outcome, resolved_at, metadata)` and evaluator `ground_truth` inputs. | `ForecastResolution.question_id` remains a compatibility alias. | Do not add resolved outcomes to forecast payloads. Outcomes remain post-forecast evaluation data. |

## Temporary Shims

Temporary shims must be small, tested, and documented in the owning package:

- `confidence` -> `probability` input compatibility is allowed for legacy callers.
- `question_id` -> `forecast_request_id` input compatibility is allowed for legacy callers.
- `reasoning_trace` remains the canonical serialized field; `reasoning`/`logical_trace`/`logical_edges` are compatibility inputs and properties only.
- `structural_trace` -> `execution_trace` input compatibility is allowed for legacy callers.
- `reporting_lane` -> `evaluation_path` input compatibility is allowed for legacy scorecard consumers.
- `confidence_interval` remains readable and writable as a deprecated interval field.

Shims must not silently change forecast meaning. Producers should not send both canonical and alias fields; if a consumer accepts both, the owning package must document and test its precedence rule.

## Compatibility Tests

Every schema-affecting change must include lightweight checks for:

1. Governance JSON schemas remain valid JSON Schema documents.
2. A governance-shaped `reasoning_trace` can be accepted by runtime models and round-tripped through the canonical serialized field.
3. Legacy `question_id`, `confidence`, `structural_trace`, `reporting_lane`, and `confidence_interval` inputs still parse while they are in the compatibility window.
4. `BetaPrior.to_distribution_dict()` produces fields accepted by `prediction.distribution`.
5. Forecast payloads keep `metadata.snapshot_time` and question `resolution_criteria` separate from evaluation `ground_truth` or `ForecastResolution` data.

## Release-Blocking Incompatibilities

Block a release if a change:

- Removes or renames a required governance field without a new schema version.
- Breaks parsing of documented v1.x aliases before their announced removal version.
- Makes `ForecastOutput.distribution` mandatory before runtime support exists.
- Emits `question_id`, `logical_trace`, `logical_edges`, `structural_trace`, or `reporting_lane` as the only supported shape after canonical replacements exist.
- Moves `snapshot_time`, `resolution_criteria`, or ground-truth resolution data across their owner objects.
- Changes the meaning or scale of `probability`, interval bounds, or Beta `alpha`/`beta`.

## Minimal Examples

Governance Forecast Object fragment:

```json
{
  "metadata": {
    "id": "forecast-1",
    "created_at": "2026-01-01T00:00:00Z",
    "snapshot_time": "2025-12-31T00:00:00Z"
  },
  "question": {
    "id": "q1",
    "title": "Will the event occur?",
    "resolution_criteria": "Resolve yes if the event occurs before the deadline."
  },
  "prediction": {
    "probability": 0.7,
    "reasoning_trace": {
      "narrative": "Evidence favors the event.",
      "causal_graph": {
        "nodes": [{"node_id": "n1", "event": "Signal observed", "probability": 0.7}],
        "edges": []
      }
    },
    "distribution": {
      "family": "beta",
      "alpha": 7.0,
      "beta": 3.0,
      "credible_interval": {"low": 0.435, "high": 0.895, "level": 0.9}
    }
  }
}
```

Runtime compatibility fragment:

```python
ForecastResult(
    forecast_request_id="q1",
    probability=0.7,
    reasoning_trace={
        "narrative": "Evidence favors the event.",
        "causal_graph": {
            "nodes": [{"node_id": "n1", "event": "Signal observed", "probability": 0.7}],
            "edges": [],
        },
    },
    execution_trace=["ingestion", "forecast"],
)
```
