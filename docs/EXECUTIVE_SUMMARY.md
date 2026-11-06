# Executive Summary

## Analytical scope

This project simulates a state-administered regulated provider network and shows how a compliance analyst can move from raw operational data to audit-ready monitoring, remediation analysis, and predictive review prioritization.

It is designed to bridge **regulatory/compliance experience** with the technical skills expected in Data Analyst and Data Scientist roles.

All data are synthetic.

## Business problem

A regulatory program may oversee hundreds of providers but have limited staff available for detailed review.

The analytical problem is therefore not simply:

> Which providers have a violation?

It is:

> How can analysts monitor compliance consistently, distinguish routine exceptions from sustained risk, and prioritize limited review capacity without turning an analytical score into an automatic enforcement decision?

## Synthetic program

The final dataset contains:

- **250 regulated providers**
- **24 monthly reporting periods**
- **6,000 provider-month observations**
- **292 material compliance findings**
- **1,046 corrective actions**
- **5,250 provider-months with a fully observed 90-day future outcome**

## Analyst workflow

The SQL monitoring layer translates compliance requirements into explicit controls covering:

- reporting timeliness
- documentation completeness
- complaint rates
- unresolved corrective actions
- repeat violations
- corrective-action aging

The project also evaluates threshold sensitivity so broad monitoring rules are not automatically treated as high-priority enforcement signals.

### Review tiers

Across 6,000 provider-months:

| Review tier | Provider-months |
| --- | ---: |
| Critical | **328** |
| High | **661** |
| Watch | **2,696** |
| Routine | **2,315** |

The corrective-action register identifies:

- **59 overdue open actions**
- **32 providers** with at least one overdue open action
- **8 high-severity actions** that are overdue and still open

## Predictive modeling

The supervised modeling task predicts whether a provider will receive a **material finding during the next three fully observed months**.

Validation uses four expanding temporal folds with a three-month embargo between training and testing.

This prevents a training observation's future-outcome window from reaching into the test period.

### Model comparison

| Model | ROC-AUC | Average precision | Brier | Log loss |
| --- | ---: | ---: | ---: | ---: |
| Prevalence only | 0.500 | 0.135 | 0.1174 | 0.3984 |
| Deterministic rules | 0.654 | 0.234 | 0.1117 | 0.3764 |
| Initial full logistic | 0.691 | 0.344 | 0.1065 | 0.3627 |
| **Preferred 10-feature logistic** | **0.728** | **0.384** | **0.1030** | **0.3495** |

A histogram gradient-boosting benchmark was also evaluated but did not outperform the preferred logistic model.

## Why the final model is lean

Feature ablation showed that removing provider type, region, and lower-value operational-scale fields improved all four validation metrics.

The preferred model uses only direct compliance measures and recent compliance history.

Provider type and region remain available for **segment auditing**, but they do not determine predicted risk.

## Decision-support value

Across 3,000 pooled out-of-time observations:

| Review capacity | Future findings captured | Precision | Lift |
| --- | ---: | ---: | ---: |
| Top 5% | **19.2%** | **52.0%** | **3.84×** |
| Top 10% | **30.3%** | **41.0%** | **3.03×** |
| Top 20% | **43.6%** | **29.5%** | **2.18×** |

The model is also well calibrated overall in the synthetic benchmark:

- calibration intercept: **-0.057**
- calibration slope: **0.991**

## Governance design

The project deliberately separates three analytical layers:

1. **Deterministic controls** provide transparent rule violations and reason codes.
2. **Predictive risk** prioritizes future review using combinations of compliance signals.
3. **Audit dimensions** such as provider type and region are used to inspect performance rather than generate risk scores.

The model prioritizes human review. It does not establish noncompliance or automate enforcement.

## Methods and tools

- SQL
- SQLite
- Python
- pandas / NumPy
- data validation
- KPI definition
- window functions
- compliance exception logic
- threshold sensitivity
- trend analysis
- temporal machine-learning validation
- logistic regression
- gradient boosting
- feature engineering
- feature ablation
- calibration
- precision / recall-oriented evaluation
- risk concentration and lift
- segment diagnostics
- automated testing
- GitHub Actions CI

## Bottom line

The analysis translates regulatory and program-domain knowledge into a structured analytics workflow.

It begins with the work expected of a compliance or data analyst—SQL controls, data validation, monitoring, remediation tracking, and reporting—and extends that foundation into temporally validated predictive modeling and model governance.
