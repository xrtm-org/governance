# The xrtm Manifesto: Forecasting is Intelligence

> "To understand reality is to predict its future."

## 1. The Core Issue
Today's AI systems (LLMs, Agents) are built and evaluated on **Fixed Knowledge**.
* **The Limitation:** Current models are tested on facts that already exist. This leads to contamination—we never know if a model is reasoning or just recalling training data.
* **The Trap:** An AI that scores 100% on a history exam hasn't proven it is intelligent; it has proven it has a memory.

## 2. The Paradigm Shift
We believe **Forecasting Future Events** is the only rigorous test of intelligence.
* **Zero Leakage:** You cannot train on next week's news. A prediction about the future is the ultimate zero-shot test because the ground truth does not exist at the moment of inference.
* **The Standard:** If an AI cannot predict what happens next, it does not truly understand what is happening now.

## 3. The Solution
**xrtm** provides the vertical infrastructure to shift AI from "Knowledge Retrieval" to "Future Prediction."
1.  **Inference:** A runtime optimized for probabilistic reasoning, not just text generation.
2.  **Evaluation:** Measuring success via **calibration** (knowing what you don't know) and **resolution** (accuracy), not semantic similarity.
3.  **Training:** Optimizing models to internalize causal chains and Bayesian logic.

## 4. The Ecosystem
We organize our Open Source Software (OSS) into a closed loop that enforces temporal integrity.

| Component | Responsibility |
| :--- | :--- |
| **xrtm-forecast** | **The Runtime.** The engine that generates predictions. It enforces rigorous reasoning, requiring the model to output causal graphs and confidence intervals before committing to a probability. |
| **xrtm-data** | **The Snapshot.** The vault that freezes the world state at specific times. It ensures we can re-run history without "future leakage" contaminating the test. |
| **xrtm-eval** | **The Judge.** The verifier that scores predictions. It handles the necessary time delay between a forecast and its resolution, using strict scoring rules (Brier, Log Loss) to measure reality. |
| **xrtm-train** | **The Learning.** The optimization layer. It uses the gap between prediction and reality to train models on causality and calibration. |
