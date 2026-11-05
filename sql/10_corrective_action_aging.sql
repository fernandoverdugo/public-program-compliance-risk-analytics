WITH as_of AS (
    SELECT date(MAX(month) || '-01', '+1 month', '-1 day') AS as_of_date
    FROM provider_months
)
SELECT
    ca.action_id,
    ca.provider_id,
    ca.opened_date,
    ca.due_date,
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
ORDER BY days_overdue DESC, action_id;
