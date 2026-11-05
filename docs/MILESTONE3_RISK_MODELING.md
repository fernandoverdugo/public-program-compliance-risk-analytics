# Milestone 3 — Predictive Compliance-Risk Modeling

## Purpose

Milestone 3 asks whether statistical or machine-learning models can improve prioritization of future material compliance findings beyond the deterministic monitoring system built in Milestones 1 and 2.

The predictive target is:

> Any material compliance finding during the next three fully observed months.

The target is only defined when all three future months are present. This avoids treating partial follow-up as a full 90-day outcome.

## Important interpretation boundary

All data in this repository are synthetic.

The simulation was designed to contain persistent but noisy compliance-risk structure through reporting delay, documentation quality, complaints, unresolved remediation, recent findings, caseload pressure, and provider-level risk.

The reported model metrics therefore demonstrate **modeling and validation methodology**, not expected performance in a real regulatory program.

## Feature design

The predictive feature set contains current-month operational indicators plus trailing three-month history.

Current measures include:

- case volume
- staffing
- caseload per staff member
- complaints and complaint rate
- report days late
- documentation completeness
- unresolved corrective actions
- current material-finding indicator

Historical measures include prior-three-month:

- complaint rate
- report delay
- documentation completeness
- unresolved corrective actions
- material findings

Provider type and region are included as categorical features.

Historical features are shifted before rolling aggregation, so the current outcome is never used to construct prior-period features.

## Temporal validation

Random train/test splits are not used.

The project uses four expanding temporal folds with a **three-month embargo** between the training cutoff and test window.

| Fold | Training through | Embargo | Test window |
| --- | --- | --- | --- |
| 1 | 2024-06 | Jul–Sep 2024 | Oct–Dec 2024 |
| 2 | 2024-09 | Oct–Dec 2024 | Jan–Mar 2025 |
| 3 | 2024-12 | Jan–Mar 2025 | Apr–Jun 2025 |
| 4 | 2025-03 | Apr–Jun 2025 | Jul–Sep 2025 |

The embargo ensures that a training observation's 90-day outcome window does not reach into the test period.

## Benchmarks

Four approaches are compared on every fold:

1. prevalence-only probability
2. deterministic rule benchmark
3. regularized logistic regression
4. histogram gradient boosting

For the deterministic benchmark, rule tiers are converted into probabilities using **training-period empirical outcome rates only**. This allows probability metrics to be compared without leaking test outcomes.

## Aggregate results

Mean performance across four temporal folds:

| Model | ROC-AUC | Average precision | Brier score | Log loss |
| --- | ---: | ---: | ---: | ---: |
| Prevalence only | 0.500 | 0.135 | 0.1174 | 0.3984 |
| Rule benchmark | 0.654 | 0.234 | 0.1117 | 0.3764 |
| **Logistic regression** | **0.691** | **0.344** | **0.1065** | **0.3627** |
| Histogram gradient boosting | 0.649 | 0.288 | 0.1159 | 0.4130 |

Logistic regression improves on the rule benchmark by approximately:

- **+0.037 ROC-AUC**
- **+0.110 average precision**
- **-0.0052 Brier score**
- **-0.0137 log loss**

Lower Brier score and log loss are better.

## Fold stability

Logistic-regression ROC-AUC ranges from **0.614 to 0.782** across the four time windows.

Average precision ranges from **0.188 to 0.422**.

This variation matters. The project does not present the mean alone as proof of stable production performance.

The earliest fold is the weakest, while the latest fold is strongest. That pattern supports continued temporal diagnostics rather than broad hyperparameter tuning.

## Feature ablation and final specification

The initial logistic benchmark used 16 features, including provider type, region, operational scale measures, and compliance-history measures.

A four-fold temporal ablation showed that the model improved when those broader descriptors were removed.

| Specification | Features | ROC-AUC | Average precision | Brier | Log loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full logistic | 16 | 0.691 | 0.344 | 0.1065 | 0.3627 |
| No provider descriptors | 14 | 0.713 | 0.375 | 0.1038 | 0.3529 |
| **Compliance core** | **10** | **0.728** | **0.384** | **0.1030** | **0.3495** |
| Compliance core, no current finding | 9 | 0.720 | 0.373 | 0.1038 | 0.3522 |

The preferred model therefore uses only direct compliance measures and recent compliance history.

Provider type and region are retained for segment auditing but excluded from prediction.

Absolute case volume, staff count, caseload per staff member, and raw complaint count are also excluded because normalized compliance measures and recent history perform better without them.

The current-month material-finding indicator is retained because scoring occurs after the monthly reporting period is complete and the model forecasts the subsequent 90 days.

The preferred specification is stored in `config/risk_model.json`.

## Final model-selection conclusion

The **10-feature regularized logistic regression** is the preferred predictive benchmark because it:

- improves all four validation metrics over the original full model;
- outperforms the deterministic rule benchmark;
- excludes provider type and region from prediction;
- relies on compliance measures that can be explained to reviewers;
- remains easier to audit than the nonlinear challenger.

Histogram gradient boosting remains documented as a nonlinear benchmark, but does not justify its added complexity here.

The deterministic rule system remains an important companion because it provides explicit control-level reason codes even when the predictive model ranks future risk more effectively.

## Next work

The next modeling phase should focus on:

- calibration diagnostics
- risk concentration / top-decile capture
- threshold selection under review-capacity constraints
- feature importance / coefficient interpretation
- model-versus-rule overlap
- subgroup and segment diagnostics
- possible anomaly detection as a separate unsupervised signal

The goal is to turn model probabilities into an explainable review-prioritization system rather than simply report an AUC.
