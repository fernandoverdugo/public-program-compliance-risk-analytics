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
| Material findings | **344** |
| Providers with any rule exception | **217** |
| Mean rule exceptions per provider | **5.73** |

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
| Critical | **382** |
| High | **682** |
| Watch | **2,676** |
| Routine | **2,260** |

The corrective-action register contains **1,022 actions**, including **26 overdue open actions** and **3 high-severity overdue open actions**.

[Read the Milestone 2 monitoring findings](docs/MILESTONE2_MONITORING.md)

## Next milestone

Milestone 3 will introduce predictive compliance-risk modeling and test whether statistical/ML models can improve future-finding prioritization beyond the deterministic monitoring benchmark.

All data are synthetic. No real program, provider, client, or case information is used.
