# xrtm Architectural Standards

**Current Status:** Enforced

To maintain a modular and zero-dependency-loop ecosystem, all components must adhere to the following strict hierarchy.

## 1. The Hierarchy of Needs (Dependency DAG)

Dependencies flow **downwards**. A component may import from layers below it, but **never** from layers above it.

| Layer | Repository | Responsibility | Allowed Imports | Forbidden Imports |
| :--- | :--- | :--- | :--- | :--- |
| **4 (Top)** | **xrtm-train** | **Orchestration.** Runs the Simulation Loop (Backtesting & Training). | `forecast`, `eval`, `data` | *(None)* |
| **3** | **xrtm-forecast** | **Inference.** The runtime engine. Generates predictions. | `eval` (for internal confidence), `data` | `train` |
| **2** | **xrtm-eval** | **Scoring.** Pure math functions. Grades the output. | `data` | `forecast` (Circular Risk!), `train` |
| **1 (Base)** | **xrtm-data** | **Definitions.** Schemas and Data Loaders. | *(None)* | `eval`, `forecast`, `train` |

## 2. The "Simulation Loop" Standard

**Rule:** Logic that iterates over time (loops) belongs exclusively in **Layer 4 (`xrtm-train`)**.

* **Why:** "Backtesting" and "Training" are modes of the same simulation loop.
* **Violation:** Placing a `backtest.py` script inside `xrtm-forecast` is forbidden, as it couples the runtime to historical data loading.

## 3. Benchmark Capability Placement

Benchmarking is an **ecosystem capability**, not a monolith inside the product
shell.

| Layer | Benchmark responsibility |
| :--- | :--- |
| `xrtm-data` | Corpus registry, provenance, license metadata, cache/import workflows, canonical question records |
| `xrtm-eval` | Scoring, calibration, comparison math, scorecard primitives |
| `xrtm-train` | Offline sweeps, replay loops, benchmark orchestration, live competition execution |
| `xrtm` | Thin user-facing inspection, reporting, and export surfaces only |

**Rule:** benchmark features must be implemented at the lowest layer that can
own them cleanly. In particular:

- corpus admissibility and provenance checks belong in `xrtm-data`
- leaderboard and benchmark math belong in `xrtm-eval`
- repeated benchmark execution belongs in `xrtm-train`
- `xrtm` may surface benchmark results, but it must not become the benchmark engine

## 4. Namespace Package Structure

All repositories must adhere to the **Implicit Namespace Package** layout to allow unified importing (`import xrtm.forecast`, `import xrtm.data`).

* **Requirement:** The folder `src/xrtm/` must **NEVER** contain an `__init__.py` file.
* **Requirement:** Each sub-package (e.g., `src/xrtm/forecast/`) **MUST** contain an `__init__.py` file.
