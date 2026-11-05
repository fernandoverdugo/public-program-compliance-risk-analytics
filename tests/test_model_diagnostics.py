import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model_diagnostics import concentration


def test_concentration_captures_highest_risk_rows():
    y = pd.Series([1, 0, 1, 0, 0])
    probability = [0.9, 0.8, 0.7, 0.2, 0.1]

    result = concentration(y, probability, 0.4)

    assert result["rows"] == 2
    assert result["positives"] == 1
    assert result["positive_capture"] == 0.5
    assert result["precision"] == 0.5


def test_preferred_model_excludes_provider_descriptors():
    import json

    config = json.loads(
        (ROOT / "config" / "risk_model.json").read_text(
            encoding="utf-8"
        )
    )
    assert "provider_type" not in config["model_features"]
    assert "region" not in config["model_features"]
    assert set(config["audit_only_features"]) == {
        "provider_type",
        "region",
    }
