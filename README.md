# Public Program Compliance Monitoring & Risk Analytics

A portfolio project simulating a state-administered regulated program to demonstrate SQL-based compliance monitoring, KPI reporting, exception detection, and predictive risk analytics.

## Core question

Which regulated entities show patterns that warrant additional compliance review, and how can limited monitoring resources be prioritized?

## Analyst layer

- SQL cohort construction
- data validation
- compliance KPIs
- exception monitoring
- overdue corrective-action tracking
- repeat-violation analysis
- dashboard-ready reporting

## Data science extension

- compliance-risk prediction
- anomaly detection
- threshold tuning
- calibration
- explainability
- temporal validation

## Initial scenario

The project simulates a network of regulated service providers with monthly operational and compliance data, including:

- case volume
- staffing and caseload pressure
- complaints
- report timeliness
- documentation completeness
- corrective actions
- material compliance findings

The first predictive outcome is whether a provider receives a material finding within the following 90 days.

## Milestone 1 — compliance monitoring foundation

**Complete**

The first analyst-facing pipeline now runs end to end:

```text
synthetic provider-month data
        ↓
SQLite compliance database
        ↓
SQL KPI monitoring
        ↓
rule-based exception table
        ↓
provider scorecard
        ↓
ranked human-review queue
```

Validated synthetic dataset:

| Measure | Result |
| --- | ---: |
| Providers | **250** |
| Provider-month rows | **6,000** |
| Months | **24** |
| Material findings | **292** |
| Providers with any rule exception | **210** |
| Mean rule exceptions per provider | **5.93** |

The monitoring layer currently flags severe late reporting, low documentation completeness, unresolved corrective actions, and elevated complaint rates.

[Read the Milestone 1 scorecard findings](docs/MILESTONE1_SCORECARD.md)

## Milestone 2 — monitoring logic and remediation analysis

**Complete**

The analyst layer now includes:

- repeat-violation logic
- 3-month trend monitoring
- control-level drilldowns
- threshold-sensitivity analysis
- transparent review severity tiers
- normalized corrective-action aging
- overdue-action monitoring
- ranked human-review queues with reason codes

Across 6,000 provider-months, the current deterministic review tiers are:

| Review tier | Provider-months |
| --- | ---: |
| Critical | **328** |
| High | **661** |
| Watch | **2,696** |
| Routine | **2,315** |

The corrective-action register contains **1,046 actions**, including **59 overdue open actions** and **8 high-severity overdue open actions**.

[Read the Milestone 2 monitoring findings](docs/MILESTONE2_MONITORING.md)

## Milestone 3 — predictive compliance-risk modeling

**Complete**

The project now predicts whether a provider will receive a material compliance finding during the next three fully observed months.

Validation uses four expanding temporal folds with a **three-month embargo** between training and testing.

| Model | ROC-AUC | Average precision | Brier score | Log loss |
| --- | ---: | ---: | ---: | ---: |
| Prevalence only | 0.500 | 0.135 | 0.1174 | 0.3984 |
| Rule benchmark | 0.654 | 0.234 | 0.1117 | 0.3764 |
| **Logistic regression** | **0.691** | **0.344** | **0.1065** | **0.3627** |
| Histogram gradient boosting | 0.649 | 0.288 | 0.1159 | 0.4130 |

Regularized logistic regression is the preferred predictive benchmark because it improves on the deterministic rules across discrimination and probability-accuracy metrics while remaining interpretable.

[Read the Milestone 3 modeling findings](docs/MILESTONE3_RISK_MODELING.md)

Because the data are synthetic, these performance metrics demonstrate methodology rather than expected real-world deployment performance.

## Next milestone

Milestone 4 will focus on model diagnostics and decision support: calibration, risk concentration, review-capacity thresholds, model-versus-rule overlap, coefficient interpretation, and segment diagnostics.

All data are synthetic. No real program, provider, client, or case information is used.
