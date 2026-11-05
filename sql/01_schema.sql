CREATE TABLE providers (
    provider_id INTEGER PRIMARY KEY,
    provider_type TEXT NOT NULL,
    region TEXT NOT NULL,
    baseline_monthly_cases INTEGER NOT NULL,
    baseline_staff INTEGER NOT NULL
);

CREATE TABLE provider_months (
    provider_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    case_volume INTEGER NOT NULL,
    staff_count INTEGER NOT NULL,
    caseload_per_staff REAL NOT NULL,
    complaints INTEGER NOT NULL,
    complaint_rate REAL NOT NULL,
    report_days_late INTEGER NOT NULL,
    documentation_complete_rate REAL NOT NULL,
    unresolved_corrective_actions INTEGER NOT NULL,
    material_finding INTEGER NOT NULL,
    future_material_finding INTEGER,
    PRIMARY KEY (provider_id, month)
);
