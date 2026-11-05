import json
from pathlib import Path

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from model_features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    load_model_frame,
)
from validate_risk_models import FOLDS, metrics, summarize


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata"

COMPLIANCE_CORE = [
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

VARIANTS = {
    "full": {
        "numeric": NUMERIC_FEATURES,
        "categorical": CATEGORICAL_FEATURES,
    },
    "without_provider_descriptors": {
        "numeric": NUMERIC_FEATURES,
        "categorical": [],
    },
    "without_current_finding": {
        "numeric": [
            feature
            for feature in NUMERIC_FEATURES
            if feature != "material_finding"
        ],
        "categorical": CATEGORICAL_FEATURES,
    },
    "without_recent_history": {
        "numeric": [
            feature
            for feature in NUMERIC_FEATURES
            if not feature.startswith("prior_3m_")
        ],
        "categorical": CATEGORICAL_FEATURES,
    },
    "compliance_core": {
        "numeric": COMPLIANCE_CORE,
        "categorical": [],
    },
    "compliance_core_without_current_finding": {
        "numeric": [
            feature
            for feature in COMPLIANCE_CORE
            if feature != "material_finding"
        ],
        "categorical": [],
    },
}


def make_pipeline(numeric_features, categorical_features):
    transformers = []

    if numeric_features:
        transformers.append(
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                numeric_features,
            )
        )

    if categorical_features:
        transformers.append(
            (
                "categorical",
                Pipeline(
                    steps=[
                        (
                            "imputer",
                            SimpleImputer(strategy="most_frequent"),
                        ),
                        (
                            "onehot",
                            OneHotEncoder(
                                handle_unknown="ignore",
                                sparse_output=False,
                            ),
                        ),
                    ]
                ),
                categorical_features,
            )
        )

    return Pipeline(
        steps=[
            (
                "preprocess",
                ColumnTransformer(transformers=transformers),
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=2000,
                    random_state=699,
                ),
            ),
        ]
    )


def evaluate_variant(frame, numeric_features, categorical_features):
    features = numeric_features + categorical_features
    runs = []

    for fold in FOLDS:
        train = frame.loc[
            (frame["month"] <= fold["train_end"])
            & frame[TARGET].notna()
        ].copy()
        test = frame.loc[
            (frame["month"] >= fold["test_start"])
            & (frame["month"] <= fold["test_end"])
            & frame[TARGET].notna()
        ].copy()

        model = make_pipeline(
            numeric_features,
            categorical_features,
        )
        model.fit(train[features], train[TARGET].astype(int))
        probability = model.predict_proba(test[features])[:, 1]

        runs.append({
            "fold": fold["name"],
            **metrics(test[TARGET].astype(int), probability),
        })

    metric_names = [
        "roc_auc",
        "average_precision",
        "brier_score",
        "log_loss",
    ]
    return {
        "feature_count": len(features),
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "metrics": {
            metric: summarize([run[metric] for run in runs])
            for metric in metric_names
        },
        "runs": runs,
    }


def main():
    frame = load_model_frame()

    results = {
        name: evaluate_variant(
            frame,
            config["numeric"],
            config["categorical"],
        )
        for name, config in VARIANTS.items()
    }

    full = results["full"]["metrics"]
    for name, result in results.items():
        result["change_from_full"] = {
            metric: (
                result["metrics"][metric]["mean"]
                - full[metric]["mean"]
            )
            for metric in full
        }

    output = {
        "target": TARGET,
        "validation": {
            "method": "four expanding temporal folds",
            "embargo_months": 3,
            "hyperparameter_retuning": False,
        },
        "variants": results,
    }

    METADATA.mkdir(parents=True, exist_ok=True)
    (METADATA / "risk_feature_ablation.json").write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
