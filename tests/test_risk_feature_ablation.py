import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ablate_risk_features import COMPLIANCE_CORE, VARIANTS


def test_compliance_core_is_lean_and_descriptor_free():
    assert len(COMPLIANCE_CORE) == 10
    assert VARIANTS["compliance_core"]["categorical"] == []
    assert "provider_type" not in COMPLIANCE_CORE
    assert "region" not in COMPLIANCE_CORE


def test_ablation_variants_are_distinct():
    assert set(VARIANTS) == {
        "full",
        "without_provider_descriptors",
        "without_current_finding",
        "without_recent_history",
        "compliance_core",
        "compliance_core_without_current_finding",
    }
