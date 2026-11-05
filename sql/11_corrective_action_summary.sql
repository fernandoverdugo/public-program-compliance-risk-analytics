WITH aging AS (
    WITH as_of AS (
        SELECT date(MAX(month) || '-01', '+1 month', '-1 day') AS as_of_date
        FROM provider_months
    )
    SELECT
        ca.action_id,
        ca.provider_id,
        ca.severity,
        ca.closed_date,
        CASE
            WHEN ca.closed_date IS NULL AND ca.due_date < as_of.as_of_date
                THEN 'overdue_open'
            WHEN ca.closed_date IS NULL
                THEN 'open_not_due'
            WHEN ca.closed_date > ca.due_date
                THEN 'closed_late'
            ELSE 'closed_on_time'
        END AS action_status,
        CAST(
            julianday(COALESCE(ca.closed_date, as_of.as_of_date))
            - julianday(ca.opened_date)
            AS INTEGER
        ) AS days_open,
        CASE
            WHEN COALESCE(ca.closed_date, as_of.as_of_date) > ca.due_date
                THEN CAST(
                    julianday(COALESCE(ca.closed_date, as_of.as_of_date))
                    - julianday(ca.due_date)
                    AS INTEGER
                )
            ELSE 0
        END AS days_overdue
    FROM corrective_actions ca
    CROSS JOIN as_of
)
SELECT
    provider_id,
    COUNT(*) AS actions_opened,
    SUM(CASE WHEN closed_date IS NULL THEN 1 ELSE 0 END) AS actions_open,
    SUM(CASE WHEN action_status = 'overdue_open' THEN 1 ELSE 0 END)
        AS overdue_open_actions,
    SUM(CASE WHEN action_status = 'closed_late' THEN 1 ELSE 0 END)
        AS actions_closed_late,
    SUM(CASE WHEN severity = 'high' THEN 1 ELSE 0 END)
        AS high_severity_actions,
    SUM(
        CASE
            WHEN severity = 'high' AND action_status = 'overdue_open'
                THEN 1
            ELSE 0
        END
    ) AS high_severity_overdue_open,
    ROUND(AVG(days_open), 1) AS avg_days_open,
    MAX(days_overdue) AS max_days_overdue
FROM aging
GROUP BY provider_id
ORDER BY overdue_open_actions DESC, actions_closed_late DESC, provider_id;
