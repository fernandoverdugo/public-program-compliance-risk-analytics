import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def summarize_dimension(frame, column):
    rows = []
    for value, group in frame.groupby(column, dropna=False):
        rows.append({
            column: value,
            "providers": int(len(group)),
            "providers_with_any_rule_exception": int(
                (group["total_rule_exceptions"] > 0).sum()
            ),
            "providers_with_material_findings": int(
                (group["material_findings"] > 0).sum()
            ),
            "mean_rule_exceptions": float(
                group["total_rule_exceptions"].mean()
            ),
            "mean_material_findings": float(
                group["material_findings"].mean()
            ),
            "mean_complaints_per_1000_cases": float(
                group["complaints_per_1000_cases"].mean()
            ),
        })
    return rows


def main():
    scorecard = pd.read_csv(PROCESSED / "provider_scorecard.csv")
    monthly = pd.read_csv(PROCESSED / "monthly_compliance_kpis.csv")

    ranked = scorecard.sort_values(
        [
            "total_rule_exceptions",
            "material_findings",
            "complaints_per_1000_cases",
        ],
        ascending=[False, False, False],
    )

    result = {
        "providers": int(len(scorecard)),
        "providers_with_any_rule_exception": int(
            (scorecard["total_rule_exceptions"] > 0).sum()
        ),
        "providers_with_material_findings": int(
            (scorecard["material_findings"] > 0).sum()
        ),
        "mean_rule_exceptions_per_provider": float(
            scorecard["total_rule_exceptions"].mean()
        ),
        "median_rule_exceptions_per_provider": float(
            scorecard["total_rule_exceptions"].median()
        ),
        "top_10_review_queue": [
            {
                "provider_id": int(row.provider_id),
                "provider_type": row.provider_type,
                "region": row.region,
                "total_rule_exceptions": int(row.total_rule_exceptions),
                "material_findings": int(row.material_findings),
                "complaints_per_1000_cases": float(
                    row.complaints_per_1000_cases
                ),
            }
            for row in ranked.head(10).itertuples(index=False)
        ],
        "by_region": summarize_dimension(scorecard, "region"),
        "by_provider_type": summarize_dimension(
            scorecard,
            "provider_type",
        ),
        "latest_month": monthly.iloc[-1].to_dict(),
    }

    (PROCESSED / "scorecard_summary.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
