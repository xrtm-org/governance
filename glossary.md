# xrtm Glossary & Terminology

This glossary defines the "Institutional Language" used across all xrtm repositories.

## Core Entities

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
*   *Analogy*: An assembly line (Graph) where an item moves to a station (Stage).

---

## Orchestration

### Orchestrator
The state-machine engine that manages workflows.
*   *Package*: `xrtm.forecast.core.orchestrator`

### GraphState
The shared memory object passed between Stages during execution.

### Stage
A single step in a workflow (implemented as a Node in the engine).

### Parallel Group
A set of Stages that execute concurrently.

### Topology
A pre-defined, reusable pattern of Stages and Edges.
*   *Package*: `xrtm.forecast.kit.topologies`

---

## Evaluation

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
The standard structured output for all predictions (see Governance schema).
*   *Package*: `xrtm.data.schemas.forecast`

### Snapshot Time
The temporal boundary for zero-leakage forecasting. No data after this time should influence predictions.

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
