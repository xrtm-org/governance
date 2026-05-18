# xrtm Glossary & Terminology

This glossary defines the "Institutional Language" used across all xrtm repositories.

## Core Entities

### Forecast Request
The canonical input object for a forecasting workflow. The historical runtime name
`ForecastQuestion` remains an allowed compatibility alias during the current
version window.
*   *Package*: `xrtm.data.core.schemas`

### Forecast Result
The canonical output object for a forecasting workflow. The historical runtime
name `ForecastOutput` remains an allowed compatibility alias during the current
version window.
*   *Package*: `xrtm.data.core.schemas`

### Agent
An autonomous software entity capable of perceiving context, reasoning via an LLM, and executing actions.
*   *Package*: `xrtm.forecast.kit.agents`

### Tool
A granular, low-level Python function that performs a single action.
*   *Analogy*: A hammer.
*   *Package*: `xrtm.forecast.core.tools`

### Skill
A high-level capability that bundles several tools and domain-specific logic.
*   *Analogy*: Carpentry (using hammer, saw, nails to build a table).
*   *Package*: `xrtm.forecast.kit.skills`

### Capability
An abstract interface allowing an Agent to acquire context from the outside world.

---

## Integration Patterns

### The Instrument Pattern (Skill/Tool)
The Agent is in charge. It decides *when* and *if* to call the logic during its reasoning loop.
*   *Analogy*: A surgeon (Agent) using a scalpel (Tool).

### The Station Pattern (Stage)
The Orchestrator is in charge. The logic runs automatically as a mandatory step in the workflow.
*   *Analogy*: An assembly line workflow where an item moves to a station (Stage).

---

## Orchestration

### Orchestrator
The state-machine engine that manages workflows.
*   *Package*: `xrtm.forecast.core.orchestrator`

### Workflow
The authored topology of stages, transitions, and policy that defines how work
should proceed.

### Run
One concrete execution of a workflow against a specific forecast request or
benchmark slice.

### Execution Trace
The ordered record of stages and runtime state transitions emitted by a run.

### GraphState
The shared memory object passed between Stages during execution. Use this term
only for the concrete runtime type; use **workflow**, **run**, or
**execution trace** for higher-level documentation.

### Stage
A single step in a workflow (implemented as a node in the engine).

### Parallel Group
A set of Stages that execute concurrently.

### Topology
A pre-defined, reusable pattern of Stages and Edges.
*   *Package*: `xrtm.forecast.kit.topologies`

---

## Evaluation

### Evaluation Path
The canonical labeled path by which a forecast result is scored, compared, or
reported. Historical names such as `reporting_lane` remain compatibility aliases
when the owning schema still supports them.

### Brier Score
The mean squared error of probabilistic predictions.
*   *Package*: `xrtm.eval.kit.eval.metrics`

### Calibration
The alignment between predicted probabilities and observed frequencies.

### Expected Calibration Error (ECE)
The weighted average gap between confidence and accuracy across bins.

---

## Data

### Forecast Object
The governance contract spanning forecast request, forecast result, reasoning
trace, and related metadata surfaces.
*   *Package*: `xrtm.data.core.schemas`

### Snapshot Time
The temporal boundary for zero-leakage forecasting. No data after this time should influence predictions.

### Reasoning Trace
The structured explanation attached to a forecast result. It may include a
qualified causal graph, but plain **graph** should not be used as the top-level
term for this surface.

### Forecast Path
The ordered reasoning path inside a forecast result's reasoning trace.

---

## Infrastructure

### Inference Provider
The adapter layer connecting the engine to an LLM backend.
*   *Package*: `xrtm.forecast.providers.inference`

### Symmetry
The guarantee that code works identically with cloud or local models.

### Telemetry (OTel)
The system for recording logs, traces, and metrics.
*   *Analogy*: The flight recorder (Black Box).
