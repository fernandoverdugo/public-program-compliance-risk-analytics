import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"


def validate_unique_keys(frame, columns, label):
    duplicates = frame.duplicated(columns).sum()
    if duplicates:
        raise RuntimeError(f"{label} contains duplicate keys: {duplicates}")


def main():
    providers = pd.read_csv(RAW / "providers.csv")
    months = pd.read_csv(RAW / "provider_months.csv")
    kpis = pd.read_csv(PROCESSED / "monthly_compliance_kpis.csv")
    exceptions = pd.read_csv(PROCESSED / "exception_monitor.csv")
    scorecard = pd.read_csv(PROCESSED / "provider_scorecard.csv")
    summary = json.loads(
        (PROCESSED / "scorecard_summary.json").read_text(encoding="utf-8")
    )
    profile = json.loads(
        (PROCESSED / "dataset_profile.json").read_text(encoding="utf-8")
    )

    validate_unique_keys(providers, ["provider_id"], "providers")
    validate_unique_keys(
        months,
        ["provider_id", "month"],
        "provider_months",
    )

    if providers["provider_id"].isna().any():
        raise RuntimeError("Provider IDs contain missing values.")

    if not months["provider_id"].isin(providers["provider_id"]).all():
        raise RuntimeError("Provider-month rows contain unknown providers.")

    if not months["documentation_complete_rate"].between(0, 1).all():
        raise RuntimeError("Documentation completeness is outside [0, 1].")

    if (months["report_days_late"] < 0).any():
        raise RuntimeError("Negative report lateness detected.")

    if (months["complaint_rate"] < 0).any():
        raise RuntimeError("Negative complaint rate detected.")

    if len(kpis) != months["month"].nunique():
        raise RuntimeError("KPI output does not contain one row per month.")

    if len(exceptions) != len(months):
        raise RuntimeError(
            "Exception monitor should contain one row per provider-month."
        )

    if len(scorecard) != len(providers):
        raise RuntimeError(
            "Provider scorecard should contain one row per provider."
        )

    if scorecard["provider_id"].duplicated().any():
        raise RuntimeError("Provider scorecard contains duplicate providers.")

    if summary["providers"] != len(providers):
        raise RuntimeError("Scorecard summary provider count mismatch.")

    if len(summary["top_10_review_queue"]) != 10:
        raise RuntimeError("Review queue should contain 10 providers.")

    if profile["providers"] != len(providers):
        raise RuntimeError("Dataset profile provider count mismatch.")

    if profile["provider_month_rows"] != len(months):
        raise RuntimeError("Dataset profile row count mismatch.")

    print("Milestone 1 data validation passed.")


if __name__ == "__main__":
    main()
