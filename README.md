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

## Milestone 1

Build and validate the synthetic provider-month dataset, load it into SQLite, and create the first compliance KPI and exception-monitoring outputs.

All data are synthetic. No real program, provider, client, or case information is used.
