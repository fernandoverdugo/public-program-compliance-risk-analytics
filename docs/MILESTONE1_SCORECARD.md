# Milestone 1 — Compliance Monitoring Scorecard

## Scope

Milestone 1 establishes the analyst-facing foundation of the project using a deterministic synthetic provider network.

The dataset contains:

- **250 regulated providers**
- **24 monthly reporting periods**
- **6,000 provider-month observations**
- **292 material compliance findings**
- **5,250 provider-months with a fully observable 90-day future outcome**

All data are synthetic and generated deterministically with seed 699.

## Core monitoring rules

The first exception-monitoring layer flags provider-months when any of the following occur:

- report submitted at least 10 days late
- documentation completeness below 90%
- at least 3 unresolved corrective actions
- complaint rate at or above 5%

These controls are transparent, reproducible SQL rules.

## Provider scorecard

The provider scorecard aggregates 24 months of monitoring history into:

- total cases
- complaints per 1,000 cases
- average reporting delay
- average documentation completeness
- maximum unresolved corrective actions
- material findings
- exception counts by rule
- total rule exceptions

Across 250 providers:

- **210 providers** generated at least one rule exception
- **129 providers** had at least one material finding
- mean rule exceptions per provider: **5.93**
- median rule exceptions per provider: **5**

The highest-ranked provider generated **47 rule exceptions** across the two-year observation period.

## Latest-month monitoring snapshot

For December 2025:

| KPI | Result |
| --- | ---: |
| Providers monitored | 250 |
| Any reporting delay | 62.0% |
| Documentation below 95% | 34.8% |
| Open corrective action | 26.4% |
| Complaints per 1,000 cases | 32.17 |
| Material finding rate | 5.6% |

These operational KPIs use broader descriptive cutoffs than the stricter review controls.

## Analyst value

Milestone 1 demonstrates the work expected in compliance-oriented analyst roles:

1. translate requirements into explicit SQL rules
2. validate source data before reporting
3. create repeatable compliance KPIs
4. build an exception-monitoring table
5. aggregate historical performance into a provider scorecard
6. rank records for human review
7. retain transparent reasons for each flag

## Status

**Complete**

Milestone 2 extends this foundation with trend analysis, repeat violations, threshold sensitivity, severity tiers, and corrective-action aging.
