SELECT
    provider_id,
    month,
    report_days_late,
    documentation_complete_rate,
    unresolved_corrective_actions,
    complaint_rate,
    CASE WHEN report_days_late >= 10 THEN 1 ELSE 0 END AS late_report_flag,
    CASE WHEN documentation_complete_rate < 0.90 THEN 1 ELSE 0 END AS documentation_flag,
    CASE WHEN unresolved_corrective_actions >= 3 THEN 1 ELSE 0 END AS corrective_action_flag,
    CASE WHEN complaint_rate >= 0.05 THEN 1 ELSE 0 END AS complaint_flag
FROM provider_months;
