WITH scored AS (
    SELECT
        provider_id,
        month,
        material_finding,
        CASE WHEN report_days_late >= 5 THEN 1 ELSE 0 END AS watch_late,
        CASE WHEN documentation_complete_rate < 0.95 THEN 1 ELSE 0 END AS watch_documentation,
        CASE WHEN unresolved_corrective_actions >= 1 THEN 1 ELSE 0 END AS watch_corrective_actions,
        CASE WHEN complaint_rate >= 0.05 THEN 1 ELSE 0 END AS watch_complaints,
        CASE WHEN report_days_late >= 10 THEN 1 ELSE 0 END AS high_late,
        CASE WHEN documentation_complete_rate < 0.90 THEN 1 ELSE 0 END AS high_documentation,
        CASE WHEN unresolved_corrective_actions >= 3 THEN 1 ELSE 0 END AS high_corrective_actions,
        CASE WHEN complaint_rate >= 0.07 THEN 1 ELSE 0 END AS high_complaints
    FROM provider_months
),
counts AS (
    SELECT
        *,
        (
            high_late
            + high_documentation
            + high_corrective_actions
            + high_complaints
        ) AS high_control_count,
        (
            watch_late
            + watch_documentation
            + watch_corrective_actions
            + watch_complaints
        ) AS watch_control_count
    FROM scored
)
SELECT
    provider_id,
    month,
    material_finding,
    watch_control_count,
    high_control_count,
    CASE
        WHEN material_finding = 1 OR high_control_count >= 2
            THEN 'critical'
        WHEN high_control_count = 1
            THEN 'high'
        WHEN watch_control_count >= 1
            THEN 'watch'
        ELSE 'routine'
    END AS review_tier,
    TRIM(
        CASE WHEN high_late = 1 THEN 'late_reporting; ' ELSE '' END
        || CASE WHEN high_documentation = 1 THEN 'documentation; ' ELSE '' END
        || CASE WHEN high_corrective_actions = 1 THEN 'corrective_actions; ' ELSE '' END
        || CASE WHEN high_complaints = 1 THEN 'complaints; ' ELSE '' END,
        '; '
    ) AS high_priority_reasons
FROM counts
ORDER BY month, provider_id;
