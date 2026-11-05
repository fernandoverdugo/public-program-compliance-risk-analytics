import json
from pathlib import Path

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from model_features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    load_model_frame,
)


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata"

FOLDS = [
    {
        "name": "fold_1",
        "train_end": "2024-06",
        "test_start": "2024-10",
        "test_end": "2024-12",
    },
    {
        "name": "fold_2",
        "train_end": "2024-09",
        "test_start": "2025-01",
        "test_end": "2025-03",
    },
    {
        "name": "fold_3",
        "train_end": "2024-12",
        "test_start": "2025-04",
        "test_end": "2025-06",
    },
    {
        "name": "fold_4",
        "train_end": "2025-03",
        "test_start": "2025-07",
        "test_end": "2025-09",
    },
]


def metrics(y_true, probability):
    probability = np.clip(probability, 1e-6, 1 - 1e-6)
    return {
        "roc_auc": float(roc_auc_score(y_true, probability)),
        "average_precision": float(
            average_precision_score(y_true, probability)
        ),
        "brier_score": float(
            brier_score_loss(y_true, probability)
        ),
        "log_loss": float(log_loss(y_true, probability)),
    }


def summarize(values):
    array = np.asarray(values, dtype=float)
    return {
        "mean": float(array.mean()),
        "std": float(array.std(ddof=1)) if len(array) > 1 else 0.0,
        "min": float(array.min()),
        "max": float(array.max()),
    }


def make_preprocessor():
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric, NUMERIC_FEATURES),
            ("categorical", categorical, CATEGORICAL_FEATURES),
        ]
    )


def make_models():
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("preprocess", make_preprocessor()),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2000,
                        random_state=699,
                    ),
                ),
            ]
        ),
        "hist_gradient_boosting": Pipeline(
            steps=[
                ("preprocess", make_preprocessor()),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        learning_rate=0.05,
                        max_iter=200,
                        max_leaf_nodes=15,
                        random_state=699,
                    ),
                ),
            ]
        ),
    }


def empirical_rule_probability(train, test):
    prevalence = float(train[TARGET].mean())
    rates = train.groupby("rule_score")[TARGET].mean().to_dict()
    return (
        test["rule_score"]
        .map(rates)
        .fillna(prevalence)
        .to_numpy(dtype=float)
    )


def evaluate_fold(frame, fold):
    train_end = fold["train_end"]
    test_start = fold["test_start"]
    test_end = fold["test_end"]

    train = frame.loc[
        (frame["month"] <= train_end)
        & frame[TARGET].notna()
    ].copy()
    test = frame.loc[
        (frame["month"] >= test_start)
        & (frame["month"] <= test_end)
        & frame[TARGET].notna()
    ].copy()

    if train["month"].max() >= test["month"].min():
        raise RuntimeError("Temporal overlap detected.")

    y_train = train[TARGET].astype(int)
    y_test = test[TARGET].astype(int)
    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES

    result = {
        "name": fold["name"],
        "train_end": train_end,
        "test_start": test_start,
        "test_end": test_end,
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "train_positive_rate": float(y_train.mean()),
        "test_positive_rate": float(y_test.mean()),
        "models": {},
    }

    prevalence_probability = np.repeat(
        float(y_train.mean()),
        len(test),
    )
    result["models"]["prevalence_only"] = metrics(
        y_test,
        prevalence_probability,
    )

    rule_probability = empirical_rule_probability(train, test)
    result["models"]["rule_benchmark"] = metrics(
        y_test,
        rule_probability,
    )

    for name, model in make_models().items():
        model.fit(train[features], y_train)
        probability = model.predict_proba(test[features])[:, 1]
        result["models"][name] = metrics(y_test, probability)

    return result


def main():
    frame = load_model_frame()
    folds = [evaluate_fold(frame, fold) for fold in FOLDS]

    model_names = [
        "prevalence_only",
        "rule_benchmark",
        "logistic_regression",
        "hist_gradient_boosting",
    ]
    metric_names = [
        "roc_auc",
        "average_precision",
        "brier_score",
        "log_loss",
    ]

    aggregate = {
        model: {
            metric: summarize(
                [
                    fold["models"][model][metric]
                    for fold in folds
                ]
            )
            for metric in metric_names
        }
        for model in model_names
    }

    result = {
        "target": TARGET,
        "target_definition": (
            "Any material compliance finding in the next three fully "
            "observed months."
        ),
        "feature_count": len(
            NUMERIC_FEATURES + CATEGORICAL_FEATURES
        ),
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "validation": {
            "method": "expanding temporal validation",
            "embargo_months": 3,
            "fold_count": len(FOLDS),
            "folds": FOLDS,
        },
        "fold_results": folds,
        "aggregate": aggregate,
    }

    METADATA.mkdir(parents=True, exist_ok=True)
    output = METADATA / "risk_model_validation.json"
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
