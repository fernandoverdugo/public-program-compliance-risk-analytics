# Milestone 2 — Monitoring Logic, Trends, and Severity Tiers

## Purpose

Milestone 2 deepens the analyst-facing layer of the project before predictive modeling begins.

The goal is to show how a compliance analyst can move from raw exceptions to a reproducible monitoring framework with:

- repeat-violation logic
- trend monitoring
- control-level drilldowns
- threshold sensitivity
- severity tiers
- transparent review reasons

## Repeat-violation logic

A provider is treated as having a repeat issue when the same control is triggered in at least three months.

Across 250 providers:

- **162** have at least one repeat issue
- **19** have repeat issues across at least two controls

Repeat-issue counts:

| Control | Providers with repeat issue |
| --- | ---: |
| Complaints | **156** |
| Corrective actions | **21** |
| Late reporting | **5** |
| Documentation | **5** |

The complaint control is intentionally the most sensitive and therefore receives additional threshold analysis rather than being treated as equally severe at every cutoff.

## Control-level event rates

Using the stricter rule thresholds from Milestone 1:

| Control | Exception events | Providers flagged | Provider-month flag rate |
| --- | ---: | ---: | ---: |
| Complaints ≥ 5% | 1,164 | 197 | 19.4% |
| Unresolved corrective actions ≥ 3 | 136 | 37 | 2.27% |
| Reporting delay ≥ 10 days | 86 | 61 | 1.43% |
| Documentation completeness < 90% | 47 | 29 | 0.78% |

The large difference in event rates demonstrates why a single generic alert threshold is inappropriate across controls.

## Threshold sensitivity

Each control is evaluated at three thresholds to show how alert volume changes.

Examples:

- late reporting: 5, 10, and 15 days
- documentation: 95%, 90%, and 85%
- unresolved corrective actions: 1, 3, and 5
- complaint rate: 3%, 5%, and 7%

The complaint control illustrates the tradeoff clearly:

| Complaint threshold | Alert events | Providers flagged | Provider-month alert rate |
| --- | ---: | ---: | ---: |
| 3% | 2,783 | 249 | 46.38% |
| 5% | 1,164 | 197 | 19.40% |
| 7% | 612 | 164 | 10.20% |

The 5% threshold is useful for broad monitoring but too common to serve as a high-priority review threshold.

## Review severity tiers

The project therefore separates **watch thresholds** from stricter **high-priority thresholds**.

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

Provider-months are then assigned:

- **Critical:** material finding or at least two high-priority controls
- **High:** exactly one high-priority control
- **Watch:** at least one watch control but no high-priority control
- **Routine:** no active watch or high-priority control

Across 6,000 provider-months:

| Review tier | Provider-months | Share |
| --- | ---: | ---: |
| Critical | **382** | 6.4% |
| High | **682** | 11.4% |
| Watch | **2,676** | 44.6% |
| Routine | **2,260** | 37.7% |

For December 2025 alone:

- 16 critical
- 26 high
- 116 watch
- 92 routine

This creates a selective review queue while preserving a broader monitoring population.

## Trend monitoring

The trend table reports monthly KPIs and three-month rolling averages.

December 2025 results include:

| KPI | Current month | 3-month average |
| --- | ---: | ---: |
| Any reporting delay | 56.8% | 57.2% |
| Documentation below 95% | 32.0% | 33.1% |
| Open corrective action | 24.8% | 25.1% |
| Complaints per 1,000 cases | 29.04 | 30.91 |
| Material finding rate | 5.6% | 4.8% |

The rolling averages make it easier to distinguish one-month noise from sustained deterioration.

## Analyst value

Milestone 2 demonstrates practical compliance-analysis judgment:

1. not every alert should be treated equally;
2. threshold selection changes workload materially;
3. repeat issues deserve different attention from isolated events;
4. operational trends need smoothing before escalation;
5. every review tier should retain an explicit reason code.

No machine-learning model is used for these tiers.

That is intentional: the deterministic monitoring system serves as the interpretable benchmark that later predictive models must outperform.

## Corrective-action aging

Milestone 2 also includes a normalized corrective-action register with:

- action opened date
- due date
- closure date
- severity
- current status
- days open
- days overdue

The synthetic program generated **1,022 corrective actions**.

Current status:

| Status | Actions |
| --- | ---: |
| Closed on time | **619** |
| Closed late | **307** |
| Open, not yet due | **70** |
| Overdue and open | **26** |

Additional review signals:

- **17 providers** currently have at least one overdue open action
- **3 high-severity actions** are both overdue and still open
- the longest overdue action in the current register is more than 200 days overdue

This adds a remediation-performance view that is distinct from the provider-month monitoring rules.

## Milestone status

**Complete**

The analyst-facing compliance-monitoring layer now includes:

- KPI reporting
- explicit SQL controls
- repeat-violation logic
- three-month trend monitoring
- threshold sensitivity
- review severity tiers
- corrective-action aging
- ranked human-review queues
- control-level reason codes

The deterministic monitoring framework now serves as the benchmark for the next phase: predictive compliance-risk modeling.
