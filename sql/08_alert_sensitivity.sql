WITH thresholds AS (
    SELECT 'late_reporting' AS control_name, 5.0 AS threshold
    UNION ALL SELECT 'late_reporting', 10.0
    UNION ALL SELECT 'late_reporting', 15.0
    UNION ALL SELECT 'documentation', 0.95
    UNION ALL SELECT 'documentation', 0.90
    UNION ALL SELECT 'documentation', 0.85
    UNION ALL SELECT 'corrective_actions', 1.0
    UNION ALL SELECT 'corrective_actions', 3.0
    UNION ALL SELECT 'corrective_actions', 5.0
    UNION ALL SELECT 'complaints', 0.03
    UNION ALL SELECT 'complaints', 0.05
    UNION ALL SELECT 'complaints', 0.07
),
evaluated AS (
    SELECT
        t.control_name,
        t.threshold,
        pm.provider_id,
        pm.month,
        CASE
            WHEN t.control_name = 'late_reporting'
                AND pm.report_days_late >= t.threshold THEN 1
            WHEN t.control_name = 'documentation'
                AND pm.documentation_complete_rate < t.threshold THEN 1
            WHEN t.control_name = 'corrective_actions'
                AND pm.unresolved_corrective_actions >= t.threshold THEN 1
            WHEN t.control_name = 'complaints'
                AND pm.complaint_rate >= t.threshold THEN 1
            ELSE 0
        END AS flag
    FROM thresholds t
    CROSS JOIN provider_months pm
)
SELECT
    control_name,
    threshold,
    SUM(flag) AS alert_events,
    COUNT(DISTINCT CASE WHEN flag = 1 THEN provider_id END)
        AS providers_flagged,
    ROUND(AVG(flag), 4) AS provider_month_alert_rate
FROM evaluated
GROUP BY control_name, threshold
ORDER BY control_name, threshold;
