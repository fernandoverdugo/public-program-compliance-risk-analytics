SELECT
    month,
    COUNT(*) AS provider_months,
    ROUND(AVG(CASE WHEN report_days_late > 0 THEN 1.0 ELSE 0.0 END), 4) AS late_report_rate,
    ROUND(AVG(CASE WHEN documentation_complete_rate < 0.95 THEN 1.0 ELSE 0.0 END), 4) AS documentation_exception_rate,
    ROUND(AVG(CASE WHEN unresolved_corrective_actions > 0 THEN 1.0 ELSE 0.0 END), 4) AS open_corrective_action_rate,
    ROUND(SUM(complaints) * 1000.0 / NULLIF(SUM(case_volume), 0), 2) AS complaints_per_1000_cases,
    ROUND(AVG(material_finding), 4) AS material_finding_rate
FROM provider_months
GROUP BY month
ORDER BY month;
