from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

NUMERIC_FEATURES = [
    "case_volume",
    "staff_count",
    "caseload_per_staff",
    "complaints",
    "complaint_rate",
    "report_days_late",
    "documentation_complete_rate",
    "unresolved_corrective_actions",
    "material_finding",
    "prior_3m_complaint_rate",
    "prior_3m_report_days_late",
    "prior_3m_documentation_complete_rate",
    "prior_3m_unresolved_corrective_actions",
    "prior_3m_material_findings",
]

CATEGORICAL_FEATURES = [
    "provider_type",
    "region",
]

TARGET = "future_material_finding"


def add_history_features(frame):
    frame = frame.sort_values(["provider_id", "month"]).copy()
    grouped = frame.groupby("provider_id", sort=False)

    specs = {
        "complaint_rate": ("prior_3m_complaint_rate", "mean"),
        "report_days_late": ("prior_3m_report_days_late", "mean"),
        "documentation_complete_rate": (
            "prior_3m_documentation_complete_rate",
            "mean",
        ),
        "unresolved_corrective_actions": (
            "prior_3m_unresolved_corrective_actions",
            "mean",
        ),
        "material_finding": ("prior_3m_material_findings", "sum"),
    }

    for source, (target, operation) in specs.items():
        if operation == "sum":
            frame[target] = grouped[source].transform(
                lambda s: s.shift(1).rolling(3, min_periods=1).sum()
            )
        else:
            frame[target] = grouped[source].transform(
                lambda s: s.shift(1).rolling(3, min_periods=1).mean()
            )

    return frame


def add_rule_score(frame):
    watch_count = (
        (frame["report_days_late"] >= 5).astype(int)
        + (frame["documentation_complete_rate"] < 0.95).astype(int)
        + (frame["unresolved_corrective_actions"] >= 1).astype(int)
        + (frame["complaint_rate"] >= 0.05).astype(int)
    )
    high_count = (
        (frame["report_days_late"] >= 10).astype(int)
        + (frame["documentation_complete_rate"] < 0.90).astype(int)
        + (frame["unresolved_corrective_actions"] >= 3).astype(int)
        + (frame["complaint_rate"] >= 0.07).astype(int)
    )

    critical = (
        (frame["material_finding"] == 1)
        | (high_count >= 2)
    )
    high = (~critical) & (high_count == 1)
    watch = (~critical) & (~high) & (watch_count >= 1)

    score = np.zeros(len(frame), dtype=float)
    score[watch.to_numpy()] = 1.0
    score[high.to_numpy()] = 2.0
    score[critical.to_numpy()] = 3.0
    frame["rule_score"] = score
    return frame


def load_model_frame():
    providers = pd.read_csv(RAW / "providers.csv")
    months = pd.read_csv(RAW / "provider_months.csv")

    frame = months.merge(
        providers[["provider_id", "provider_type", "region"]],
        on="provider_id",
        how="left",
        validate="many_to_one",
    )
    frame = add_history_features(frame)
    frame = add_rule_score(frame)
    frame["month_period"] = pd.PeriodIndex(frame["month"], freq="M")
    return frame
