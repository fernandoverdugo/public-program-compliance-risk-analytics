import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def markdown_paths(text):
    targets = re.findall(r"!?(?:\[[^\]]*\])\(([^)]+)\)", text)
    result = []
    for target in targets:
        target = target.strip()
        if (
            target.startswith("http://")
            or target.startswith("https://")
            or target.startswith("#")
            or target.startswith("mailto:")
        ):
            continue
        path = target.split("#", 1)[0]
        if path:
            result.append(path)
    return result


def validate_markdown_links():
    markdown_files = [ROOT / "README.md"] + sorted(
        (ROOT / "docs").glob("*.md")
    )
    missing = []

    for markdown in markdown_files:
        text = markdown.read_text(encoding="utf-8")
        for target in markdown_paths(text):
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                missing.append(
                    f"{markdown.relative_to(ROOT)} -> {target}"
                )

    if missing:
        raise RuntimeError(
            "Broken internal markdown links:\n"
            + "\n".join(missing)
        )


def validate_required_artifacts():
    required = [
        "config/risk_model.json",
        "data/metadata/scorecard_summary.json",
        "data/metadata/milestone2_summary.json",
        "data/metadata/risk_model_validation.json",
        "data/metadata/risk_feature_ablation.json",
        "data/metadata/model_diagnostics.json",
        "docs/EXECUTIVE_SUMMARY.md",
        "docs/MILESTONE1_SCORECARD.md",
        "docs/MILESTONE2_MONITORING.md",
        "docs/MILESTONE3_RISK_MODELING.md",
        "docs/MILESTONE4_MODEL_DIAGNOSTICS.md",
        "docs/figures/review_tiers.svg",
        "docs/figures/model_comparison.svg",
        "docs/figures/review_capacity.svg",
        "sql/09_severity_tiers.sql",
        "sql/10_corrective_action_aging.sql",
        "src/validate_risk_models.py",
        "src/model_diagnostics.py",
        "src/ablate_risk_features.py",
    ]
    missing = [
        path for path in required
        if not (ROOT / path).exists()
    ]
    if missing:
        raise RuntimeError(
            "Missing required project artifacts: "
            + ", ".join(missing)
        )


def validate_preferred_model():
    config = json.loads(
        (ROOT / "config" / "risk_model.json").read_text(
            encoding="utf-8"
        )
    )
    ablation = json.loads(
        (
            ROOT
            / "data"
            / "metadata"
            / "risk_feature_ablation.json"
        ).read_text(encoding="utf-8")
    )
    diagnostics = json.loads(
        (
            ROOT
            / "data"
            / "metadata"
            / "model_diagnostics.json"
        ).read_text(encoding="utf-8")
    )

    if config["status"] != "validated_preferred_compliance_risk_benchmark":
        raise RuntimeError("Preferred model is not marked as validated.")

    if len(config["model_features"]) != 10:
        raise RuntimeError("Preferred model must contain 10 features.")

    if set(config["model_features"]) & set(config["audit_only_features"]):
        raise RuntimeError(
            "Predictive and audit-only feature sets overlap."
        )

    preferred = ablation["variants"]["compliance_core"]
    if set(preferred["numeric_features"]) != set(config["model_features"]):
        raise RuntimeError(
            "Preferred feature set differs from ablation result."
        )

    expected = config["validation"]["mean_metrics"]
    for metric, value in expected.items():
        actual = preferred["metrics"][metric]["mean"]
        if abs(actual - value) > 1e-12:
            raise RuntimeError(
                f"Config metric mismatch for {metric}."
            )

    if diagnostics["model_version"] != config["version"]:
        raise RuntimeError(
            "Diagnostics model version differs from config."
        )

    if diagnostics["out_of_time_rows"] != 3000:
        raise RuntimeError(
            "Unexpected pooled out-of-time row count."
        )

    if len(diagnostics["pooled_capacity"]) != 3:
        raise RuntimeError(
            "Expected 5%, 10%, and 20% capacity results."
        )


def main():
    validate_required_artifacts()
    validate_preferred_model()
    validate_markdown_links()
    print("Project integrity validation passed.")


if __name__ == "__main__":
    main()
