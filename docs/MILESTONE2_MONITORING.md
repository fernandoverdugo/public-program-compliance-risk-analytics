# Milestone 2 — Monitoring Logic, Trends, and Remediation

## Purpose

Milestone 2 deepens the analyst-facing monitoring framework before predictive modeling.

It adds:

- repeat-violation logic
- 3-month trend monitoring
- control-level drilldowns
- threshold-sensitivity analysis
- transparent severity tiers
- corrective-action aging
- ranked review queues with reason codes

## Repeat violations

A provider is treated as having a repeat issue when the same control is triggered in at least three months.

Across 250 providers:

- **154** have at least one repeat issue
- **20** have repeat issues across at least two controls

| Control | Providers with repeat issue |
| --- | ---: |
| Complaints | **152** |
| Corrective actions | **17** |
| Late reporting | **7** |
| Documentation | **7** |

## Control-level event rates

Using the stricter review thresholds:

| Control | Exception events | Providers flagged | Provider-month flag rate |
| --- | ---: | ---: | ---: |
| Complaints ≥ 5% | 1,170 | 185 | 19.50% |
| Unresolved corrective actions ≥ 3 | 142 | 35 | 2.37% |
| Reporting delay ≥ 10 days | 104 | 64 | 1.73% |
| Documentation completeness < 90% | 67 | 29 | 1.12% |

The variation in alert volumes is why thresholds are evaluated separately by control.

## Threshold sensitivity

The complaint control illustrates the workload tradeoff:

| Complaint threshold | Alert events | Providers flagged | Provider-month alert rate |
| --- | ---: | ---: | ---: |
| 3% | 2,779 | 248 | 46.32% |
| 5% | 1,170 | 185 | 19.50% |
| 7% | 634 | 151 | 10.57% |

Similar sensitivity tables are produced for reporting delay, documentation completeness, and unresolved corrective actions.

## Review severity tiers

### Watch thresholds

- reporting delay ≥ 5 days
- documentation completeness < 95%
- at least 1 unresolved corrective action
- complaint rate ≥ 5%

### High thresholds

- reporting delay ≥ 10 days
- documentation completeness < 90%
- at least 3 unresolved corrective actions
- complaint rate ≥ 7%

Provider-months are assigned:

- **Critical:** material finding or at least two high-priority controls
- **High:** exactly one high-priority control
- **Watch:** at least one watch control but no high-priority control
- **Routine:** no watch or high-priority control

Across 6,000 provider-months:

| Review tier | Provider-months | Share |
| --- | ---: | ---: |
| Critical | **328** | 5.5% |
| High | **661** | 11.0% |
| Watch | **2,696** | 44.9% |
| Routine | **2,315** | 38.6% |

For December 2025:

- 16 critical
- 25 high
- 115 watch
- 94 routine

## Corrective-action aging

The normalized corrective-action register contains **1,046 actions** with opened, due, and closure dates plus severity.

| Status | Actions |
| --- | ---: |
| Closed on time | **606** |
| Closed late | **310** |
| Open, not yet due | **71** |
| Overdue and open | **59** |

Additional review signals:

- **32 providers** currently have at least one overdue open action
- **8 high-severity actions** are overdue and still open
- the most overdue records exceed 300 days past due

## Trend monitoring

December 2025:

| KPI | Current month | 3-month average |
| --- | ---: | ---: |
| Any reporting delay | 62.0% | 60.0% |
| Documentation below 95% | 34.8% | 34.8% |
| Open corrective action | 26.4% | 26.8% |
| Complaints per 1,000 cases | 32.17 | 32.00 |
| Material finding rate | 5.6% | 4.7% |

## Analyst value

The milestone shows that:

1. alert volume changes materially with threshold choice;
2. repeat issues should be distinguished from isolated exceptions;
3. broad monitoring thresholds should not automatically become enforcement thresholds;
4. trend smoothing helps separate noise from sustained deterioration;
5. remediation aging adds a different risk dimension from monthly controls;
6. every severity tier can retain an explicit reason code.

No machine-learning model is used for the deterministic tiers.

## Status

**Complete**

This monitoring framework is the benchmark that Milestone 3 predictive models must outperform.
