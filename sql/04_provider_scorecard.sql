WITH history AS (
    SELECT
        pm.provider_id,
        p.provider_type,
        p.region,
        COUNT(*) AS months_observed,
        SUM(pm.case_volume) AS total_cases,
        SUM(pm.complaints) AS total_complaints,
        AVG(pm.report_days_late) AS avg_report_days_late,
        AVG(pm.documentation_complete_rate) AS avg_documentation_complete_rate,
        MAX(pm.unresolved_corrective_actions) AS max_unresolved_corrective_actions,
        SUM(pm.material_finding) AS material_findings,
        SUM(CASE WHEN pm.report_days_late >= 10 THEN 1 ELSE 0 END)
            AS late_report_exceptions,
        SUM(CASE WHEN pm.documentation_complete_rate < 0.90 THEN 1 ELSE 0 END)
            AS documentation_exceptions,
        SUM(CASE WHEN pm.unresolved_corrective_actions >= 3 THEN 1 ELSE 0 END)
            AS corrective_action_exceptions,
        SUM(CASE WHEN pm.complaint_rate >= 0.05 THEN 1 ELSE 0 END)
            AS complaint_exceptions
    FROM provider_months pm
    JOIN providers p
      ON p.provider_id = pm.provider_id
    GROUP BY
        pm.provider_id,
        p.provider_type,
        p.region
)
SELECT
    provider_id,
    provider_type,
    region,
    months_observed,
    total_cases,
    total_complaints,
    ROUND(total_complaints * 1000.0 / NULLIF(total_cases, 0), 2)
        AS complaints_per_1000_cases,
    ROUND(avg_report_days_late, 2) AS avg_report_days_late,
    ROUND(avg_documentation_complete_rate, 4)
        AS avg_documentation_complete_rate,
    max_unresolved_corrective_actions,
    material_findings,
    late_report_exceptions,
    documentation_exceptions,
    corrective_action_exceptions,
    complaint_exceptions,
    (
        late_report_exceptions
        + documentation_exceptions
        + corrective_action_exceptions
        + complaint_exceptions
    ) AS total_rule_exceptions
FROM history
ORDER BY total_rule_exceptions DESC, material_findings DESC, provider_id;
