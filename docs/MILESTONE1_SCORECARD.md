# Milestone 1 — Compliance Monitoring Scorecard

## Scope

Milestone 1 establishes the analyst-facing foundation of the project.

The synthetic program contains:

- **250 regulated providers**
- **24 monthly reporting periods**
- **6,000 provider-month observations**
- **344 material compliance findings**
- **5,750 rows with an observable 90-day future-outcome window**

All data are synthetic and generated deterministically with seed 699.

## Core monitoring rules

The first exception-monitoring layer flags provider-months when any of the following occur:

- report submitted at least 10 days late
- documentation completeness below 90%
- at least 3 unresolved corrective actions
- complaint rate at or above 5%

These rules are intentionally transparent and auditable.

## Provider scorecard

The provider-level scorecard aggregates 24 months of monitoring history into:

- total cases
- complaints per 1,000 cases
- average reporting delay
- average documentation completeness
- maximum unresolved corrective actions
- material findings
- exception counts by rule
- total rule exceptions

The scorecard produces a ranked review queue for analyst follow-up.

## Initial results

Across 250 providers:

- **217 providers** generated at least one rule exception
- **180 providers** had at least one material finding
- mean rule exceptions per provider: **5.73**
- median rule exceptions per provider: **5**

The highest-ranked provider generated **26 rule exceptions** across the two-year observation period.

The top review queue is deliberately based on transparent rule activity rather than a machine-learning score at this stage.

## Latest-month monitoring snapshot

For December 2025:

| KPI | Result |
| --- | ---: |
| Providers monitored | 250 |
| Any reporting delay | 56.8% |
| Documentation below 95% | 32.0% |
| Open corrective action | 24.8% |
| Complaints per 1,000 cases | 29.04 |
| Material finding rate | 5.6% |

The broader KPI thresholds above are descriptive operational measures. They should not be confused with the stricter exception thresholds used for the review queue.

## Segment observations

Regional mean rule-exception counts are relatively close, ranging from **5.09** in Central to **6.13** in North.

By provider type:

- Community: 5.49 mean rule exceptions
- Regional: 6.41
- Specialty: 5.29

Regional providers also show the highest mean complaint rate at approximately **42.9 complaints per 1,000 cases**.

Because this is synthetic data, these differences demonstrate analytical workflow rather than real-world geographic or provider-type disparities.

## Analyst value

Milestone 1 demonstrates the core work expected in compliance-oriented analyst roles:

1. translate monitoring requirements into explicit SQL rules
2. validate source data before reporting
3. create repeatable compliance KPIs
4. build an exception-monitoring table
5. aggregate historical performance into a provider scorecard
6. rank records for human review
7. preserve transparent reasons for each flag

## Next milestone

Milestone 2 will strengthen the analyst layer before predictive modeling by adding:

- trend analysis
- repeat-violation logic
- corrective-action aging
- severity tiers
- control-level drilldowns
- alert-volume sensitivity
- dashboard-ready summary tables

Predictive risk modeling will follow only after the deterministic monitoring system is mature.
