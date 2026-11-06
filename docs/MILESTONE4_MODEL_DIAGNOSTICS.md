# Milestone 4 — Model Diagnostics & Decision Support

## Purpose

Milestone 4 converts the preferred risk model from a modeling benchmark into an explainable review-prioritization tool.

The analysis uses pooled out-of-time predictions from the four embargoed temporal test windows. No test observation is used to fit the model that scores it.

## Preferred model

The selected model is the 10-feature regularized logistic regression defined in `config/risk_model.json`.

It uses direct compliance measures and recent compliance history only.

Provider type and region are excluded from prediction and retained strictly for segment auditing.

## Pooled out-of-time performance

Across **3,000** out-of-time provider-months:

- future-finding positives: **406**
- prevalence: **13.5%**
- ROC-AUC: **0.727**
- average precision: **0.371**
- Brier score: **0.1030**
- log loss: **0.3495**

The pooled ROC-AUC differs slightly from the mean fold ROC-AUC because pooled evaluation combines all out-of-time observations before computing the metric.

## Review-capacity analysis

The model is evaluated at several review-capacity levels.

| Review capacity | Rows reviewed | Findings captured | Precision | Lift |
| --- | ---: | ---: | ---: | ---: |
| Top 5% | 150 | **19.2%** | **52.0%** | **3.84×** |
| Top 10% | 300 | **30.3%** | **41.0%** | **3.03×** |
| Top 20% | 600 | **43.6%** | **29.5%** | **2.18×** |

This is a more operational interpretation than ROC-AUC alone.

For example, if analysts could review only the highest-risk 10% of provider-months, the synthetic benchmark indicates that roughly **30% of subsequent material findings** would fall inside that queue.

## Temporal stability of top-decile capture

Top-10% finding capture varies across time:

- Fold 1: 22.4%
- Fold 2: 32.2%
- Fold 3: 26.5%
- Fold 4: 39.8%

This variability is retained in the repository rather than reporting only the pooled result.

## Calibration

Pooled calibration diagnostics:

- intercept: **-0.057**
- slope: **0.991**

Ideal values are approximately 0 and 1.

The preferred model is therefore well calibrated overall in the synthetic out-of-time sample, although individual probability bins still show normal sampling variation.

The highest predicted-risk decile averages a predicted probability of approximately **43.7%** with an observed future-finding rate of **41.0%**.

## Model versus deterministic rules

The model is not intended to replace the rule system.

Within each temporal fold, the share of the model's highest-risk 10% that is also classified as high/critical by deterministic rules ranges from:

- 49.3% in Fold 1
- 65.3% in Fold 2
- 72.0% in Fold 3
- 68.0% in Fold 4

This means the two approaches overlap substantially but are not redundant.

The deterministic system contributes explicit control reasons, while the predictive model can identify combinations of weaker signals that collectively indicate elevated future risk.

## Segment audit

Provider type and region are excluded from prediction but retained for performance auditing.

### Provider type

| Provider type | Rows | Positives | ROC-AUC | Average precision |
| --- | ---: | ---: | ---: | ---: |
| Community | 1,716 | 253 | **0.761** | **0.427** |
| Regional | 876 | 114 | **0.716** | **0.378** |
| Specialty | 408 | 39 | **0.581** | **0.112** |

Performance is notably weaker for the smaller Specialty segment.

Because the data are synthetic, this is not evidence of real-world disparate performance. It illustrates why segment-specific validation remains necessary even when segment descriptors are excluded from model inputs.

### Region

Regional ROC-AUC ranges from approximately **0.703 to 0.737**, with less variation than provider type.

## Coefficient review

The strongest standardized signals in the latest training window include:

- lower prior-three-month documentation completeness
- higher prior-three-month complaint rate
- more unresolved corrective actions
- a current material finding
- more material findings in the prior three months
- higher current complaint rate

These directions align with the simulated compliance-risk process and are easier to explain than the original model's spurious geographic coefficients.

Coefficient magnitude is descriptive, not causal.

## Governance interpretation

The preferred workflow deliberately separates three layers:

1. **Deterministic controls** — explicit rule violations and reason codes.
2. **Predictive risk** — future-finding prioritization using compliance history.
3. **Audit dimensions** — provider type and region used to inspect differential performance.

This design allows predictive ranking to add value without turning the model into an automated compliance determination.

## Status

**Complete**

Milestone 4 establishes:

- capacity-based review analysis
- risk concentration and lift
- calibration diagnostics
- model-versus-rule overlap
- segment auditing
- coefficient interpretation
- a validated lean model specification

An optional analytical extension is anomaly detection as a separate unsupervised signal. The current analysis, figures, executive summary, and validation workflow are complete.
