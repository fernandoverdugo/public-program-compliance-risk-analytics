import json
import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
DB = PROCESSED / "compliance.db"


def execute_script(connection, path):
    connection.executescript(path.read_text(encoding="utf-8"))


def main():
    providers_path = RAW / "providers.csv"
    months_path = RAW / "provider_months.csv"

    if not providers_path.exists() or not months_path.exists():
        raise FileNotFoundError(
            "Synthetic CSV files are missing. Run generate_synthetic_data.py first."
        )

    PROCESSED.mkdir(parents=True, exist_ok=True)

    providers = pd.read_csv(providers_path)
    provider_months = pd.read_csv(months_path)

    if DB.exists():
        DB.unlink()

    with sqlite3.connect(DB) as connection:
        execute_script(connection, ROOT / "sql" / "01_schema.sql")
        providers.to_sql(
            "providers",
            connection,
            if_exists="append",
            index=False,
        )
        provider_months.to_sql(
            "provider_months",
            connection,
            if_exists="append",
            index=False,
        )

        kpis = pd.read_sql_query(
            (ROOT / "sql" / "02_compliance_kpis.sql").read_text(
                encoding="utf-8"
            ),
            connection,
        )
        exceptions = pd.read_sql_query(
            (ROOT / "sql" / "03_exception_monitor.sql").read_text(
                encoding="utf-8"
            ),
            connection,
        )
        scorecard = pd.read_sql_query(
            (ROOT / "sql" / "04_provider_scorecard.sql").read_text(
                encoding="utf-8"
            ),
            connection,
        )

    kpis.to_csv(PROCESSED / "monthly_compliance_kpis.csv", index=False)
    exceptions.to_csv(PROCESSED / "exception_monitor.csv", index=False)
    scorecard.to_csv(PROCESSED / "provider_scorecard.csv", index=False)

    summary = {
        "providers": int(len(providers)),
        "provider_month_rows": int(len(provider_months)),
        "months": int(provider_months["month"].nunique()),
        "material_findings": int(provider_months["material_finding"].sum()),
        "future_outcome_observed_rows": int(
            provider_months["future_material_finding"].notna().sum()
        ),
        "exception_rows": int(
            (
                exceptions[
                    [
                        "late_report_flag",
                        "documentation_flag",
                        "corrective_action_flag",
                        "complaint_flag",
                    ]
                ].sum(axis=1)
                > 0
            ).sum()
        ),
        "providers_with_any_rule_exception": int(
            (scorecard["total_rule_exceptions"] > 0).sum()
        ),
        "providers_with_material_findings": int(
            (scorecard["material_findings"] > 0).sum()
        ),
    }

    (PROCESSED / "dataset_profile.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
