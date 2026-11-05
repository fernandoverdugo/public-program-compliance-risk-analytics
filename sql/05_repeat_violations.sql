WITH flags AS (
    SELECT
        provider_id,
        month,
        CASE WHEN report_days_late >= 10 THEN 1 ELSE 0 END AS late_report_flag,
        CASE WHEN documentation_complete_rate < 0.90 THEN 1 ELSE 0 END AS documentation_flag,
        CASE WHEN unresolved_corrective_actions >= 3 THEN 1 ELSE 0 END AS corrective_action_flag,
        CASE WHEN complaint_rate >= 0.05 THEN 1 ELSE 0 END AS complaint_flag
    FROM provider_months
),
provider_counts AS (
    SELECT
        provider_id,
        SUM(late_report_flag) AS late_report_events,
        SUM(documentation_flag) AS documentation_events,
        SUM(corrective_action_flag) AS corrective_action_events,
        SUM(complaint_flag) AS complaint_events
    FROM flags
    GROUP BY provider_id
)
SELECT
    provider_id,
    late_report_events,
    documentation_events,
    corrective_action_events,
    complaint_events,
    CASE WHEN late_report_events >= 3 THEN 1 ELSE 0 END AS repeat_late_reporting,
    CASE WHEN documentation_events >= 3 THEN 1 ELSE 0 END AS repeat_documentation_issue,
    CASE WHEN corrective_action_events >= 3 THEN 1 ELSE 0 END AS repeat_corrective_action_issue,
    CASE WHEN complaint_events >= 3 THEN 1 ELSE 0 END AS repeat_complaint_issue,
    (
        CASE WHEN late_report_events >= 3 THEN 1 ELSE 0 END
        + CASE WHEN documentation_events >= 3 THEN 1 ELSE 0 END
        + CASE WHEN corrective_action_events >= 3 THEN 1 ELSE 0 END
        + CASE WHEN complaint_events >= 3 THEN 1 ELSE 0 END
    ) AS repeat_control_count
FROM provider_counts
ORDER BY repeat_control_count DESC, provider_id;
