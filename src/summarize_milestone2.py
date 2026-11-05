import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def main():
    repeat_violations = pd.read_csv(
        PROCESSED / "repeat_violations.csv"
    )
    trends = pd.read_csv(PROCESSED / "compliance_trends.csv")
    control_summary = pd.read_csv(
        PROCESSED / "control_summary.csv"
    )
    sensitivity = pd.read_csv(
        PROCESSED / "alert_sensitivity.csv"
    )

    repeat_columns = [
        "repeat_late_reporting",
        "repeat_documentation_issue",
        "repeat_corrective_action_issue",
        "repeat_complaint_issue",
    ]

    result = {
        "providers_with_repeat_issue": int(
            (repeat_violations["repeat_control_count"] > 0).sum()
        ),
        "providers_with_multiple_repeat_controls": int(
            (repeat_violations["repeat_control_count"] >= 2).sum()
        ),
        "repeat_issue_counts": {
            column: int(repeat_violations[column].sum())
            for column in repeat_columns
        },
        "control_summary": control_summary.to_dict(
            orient="records"
        ),
        "alert_sensitivity": sensitivity.to_dict(
            orient="records"
        ),
        "latest_trend": trends.iloc[-1].to_dict(),
        "previous_3m_trend": trends.iloc[-4].to_dict()
        if len(trends) >= 4
        else None,
    }

    (PROCESSED / "milestone2_summary.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
