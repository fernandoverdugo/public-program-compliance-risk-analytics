WITH controls AS (
    SELECT
        provider_id,
        'late_reporting' AS control_name,
        CASE WHEN report_days_late >= 10 THEN 1 ELSE 0 END AS flag
    FROM provider_months
    UNION ALL
    SELECT
        provider_id,
        'documentation',
        CASE WHEN documentation_complete_rate < 0.90 THEN 1 ELSE 0 END
    FROM provider_months
    UNION ALL
    SELECT
        provider_id,
        'corrective_actions',
        CASE WHEN unresolved_corrective_actions >= 3 THEN 1 ELSE 0 END
    FROM provider_months
    UNION ALL
    SELECT
        provider_id,
        'complaints',
        CASE WHEN complaint_rate >= 0.05 THEN 1 ELSE 0 END
    FROM provider_months
)
SELECT
    control_name,
    SUM(flag) AS exception_events,
    COUNT(DISTINCT CASE WHEN flag = 1 THEN provider_id END)
        AS providers_flagged,
    ROUND(AVG(flag), 4) AS provider_month_flag_rate
FROM controls
GROUP BY control_name
ORDER BY exception_events DESC;
