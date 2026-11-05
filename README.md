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

## Next milestone

Milestone 2 will deepen the analyst layer with trend analysis, repeat-violation logic, corrective-action aging, severity tiers, control drilldowns, and alert-volume sensitivity before predictive modeling begins.

All data are synthetic. No real program, provider, client, or case information is used.
