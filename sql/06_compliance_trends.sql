WITH monthly AS (
    SELECT
        month,
        AVG(CASE WHEN report_days_late > 0 THEN 1.0 ELSE 0.0 END)
            AS late_report_rate,
        AVG(CASE WHEN documentation_complete_rate < 0.95 THEN 1.0 ELSE 0.0 END)
            AS documentation_exception_rate,
        AVG(CASE WHEN unresolved_corrective_actions > 0 THEN 1.0 ELSE 0.0 END)
            AS open_corrective_action_rate,
        SUM(complaints) * 1000.0 / NULLIF(SUM(case_volume), 0)
            AS complaints_per_1000_cases,
        AVG(material_finding) AS material_finding_rate
    FROM provider_months
    GROUP BY month
)
SELECT
    month,
    ROUND(late_report_rate, 4) AS late_report_rate,
    ROUND(
        AVG(late_report_rate) OVER (
            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS late_report_rate_3m,
    ROUND(documentation_exception_rate, 4)
        AS documentation_exception_rate,
    ROUND(
        AVG(documentation_exception_rate) OVER (
            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS documentation_exception_rate_3m,
    ROUND(open_corrective_action_rate, 4)
        AS open_corrective_action_rate,
    ROUND(
        AVG(open_corrective_action_rate) OVER (
            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS open_corrective_action_rate_3m,
    ROUND(complaints_per_1000_cases, 2)
        AS complaints_per_1000_cases,
    ROUND(
        AVG(complaints_per_1000_cases) OVER (
            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS complaints_per_1000_cases_3m,
    ROUND(material_finding_rate, 4) AS material_finding_rate,
    ROUND(
        AVG(material_finding_rate) OVER (
            ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS material_finding_rate_3m
FROM monthly
ORDER BY month;
