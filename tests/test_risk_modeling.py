import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model_features import add_history_features, add_rule_score
from validate_risk_models import FOLDS


def test_temporal_folds_have_three_month_embargo():
    for fold in FOLDS:
        train_end = pd.Period(fold["train_end"], freq="M")
        test_start = pd.Period(fold["test_start"], freq="M")
        assert test_start - train_end == 4


def test_history_features_use_prior_months_only():
    frame = pd.DataFrame(
        {
            "provider_id": [1, 1, 1, 1],
            "month": ["2024-01", "2024-02", "2024-03", "2024-04"],
            "complaint_rate": [0.01, 0.02, 0.03, 0.04],
            "report_days_late": [1, 2, 3, 4],
            "documentation_complete_rate": [0.99, 0.98, 0.97, 0.96],
            "unresolved_corrective_actions": [0, 1, 2, 3],
            "material_finding": [0, 0, 1, 0],
        }
    )
    result = add_history_features(frame)
    fourth = result.iloc[3]

    assert fourth["prior_3m_complaint_rate"] == 0.02
    assert fourth["prior_3m_material_findings"] == 1


def test_rule_score_is_ordered():
    frame = pd.DataFrame(
        {
            "report_days_late": [0, 6, 11, 12],
            "documentation_complete_rate": [0.99, 0.96, 0.96, 0.88],
            "unresolved_corrective_actions": [0, 0, 0, 3],
            "complaint_rate": [0.01, 0.01, 0.01, 0.08],
            "material_finding": [0, 0, 0, 1],
        }
    )
    result = add_rule_score(frame)
    assert result["rule_score"].tolist() == [0.0, 1.0, 2.0, 3.0]
