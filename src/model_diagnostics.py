import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from model_features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    load_model_frame,
)
from validate_risk_models import FOLDS, make_models, metrics


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata"
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def concentration(y, probability, fraction):
    probability = np.asarray(probability, dtype=float)
    count = max(1, int(math.ceil(len(y) * fraction)))
    order = np.argsort(-probability)
    selected = order[:count]
    positives = int(y.iloc[selected].sum())
    total_positives = int(y.sum())
    precision = float(y.iloc[selected].mean())
    prevalence = float(y.mean())
    return {
        "fraction": fraction,
        "rows": count,
        "positives": positives,
        "positive_capture": (
            float(positives / total_positives)
            if total_positives
            else None
        ),
        "precision": precision,
        "lift": (
            float(precision / prevalence)
            if prevalence > 0
            else None
        ),
    }


def calibration_summary(frame):
    probability = np.clip(
        frame["probability"].to_numpy(dtype=float),
        1e-6,
        1 - 1e-6,
    )
    y = frame[TARGET].astype(int).to_numpy()
    logit = np.log(probability / (1 - probability)).reshape(-1, 1)

    calibration = LogisticRegression(
        C=1e6,
        solver="lbfgs",
        max_iter=2000,
    )
    calibration.fit(logit, y)

    bins = frame.copy()
    bins["bin"] = pd.qcut(
        bins["probability"],
        q=10,
        duplicates="drop",
    )
    grouped = (
        bins.groupby("bin", observed=True)
        .agg(
            rows=(TARGET, "size"),
            mean_probability=("probability", "mean"),
            observed_rate=(TARGET, "mean"),
        )
        .reset_index(drop=True)
    )

    return {
        "intercept": float(calibration.intercept_[0]),
        "slope": float(calibration.coef_[0][0]),
        "bins": [
            {
                "rows": int(row.rows),
                "mean_probability": float(row.mean_probability),
                "observed_rate": float(row.observed_rate),
            }
            for row in grouped.itertuples(index=False)
        ],
    }


def segment_metrics(frame, column):
    result = {}
    for value, group in frame.groupby(column):
        y = group[TARGET].astype(int)
        if len(group) < 100 or y.sum() < 10 or y.nunique() < 2:
            result[str(value)] = {
                "rows": int(len(group)),
                "positives": int(y.sum()),
                "status": "insufficient_events",
            }
            continue

        result[str(value)] = {
            "rows": int(len(group)),
            "positives": int(y.sum()),
            "status": "reported",
            **metrics(y, group["probability"].to_numpy()),
        }
    return result


def fit_latest_coefficients(frame):
    fold = FOLDS[-1]
    train = frame.loc[
        (frame["month"] <= fold["train_end"])
        & frame[TARGET].notna()
    ].copy()

    model = make_models()["logistic_regression"]
    model.fit(train[FEATURES], train[TARGET].astype(int))

    names = model.named_steps["preprocess"].get_feature_names_out()
    coefficients = model.named_steps["model"].coef_[0]

    rows = [
        {
            "feature": str(name),
            "coefficient": float(coefficient),
            "absolute_coefficient": float(abs(coefficient)),
        }
        for name, coefficient in zip(names, coefficients)
    ]
    rows.sort(
        key=lambda item: item["absolute_coefficient"],
        reverse=True,
    )

    return {
        "training_through": fold["train_end"],
        "note": (
            "Numeric coefficients are standardized by the modeling pipeline; "
            "categorical coefficients are relative to one-hot encoded levels."
        ),
        "top_coefficients": rows[:20],
    }


def main():
    frame = load_model_frame()
    pooled = []
    fold_diagnostics = []

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

        model = make_models()["logistic_regression"]
        model.fit(train[FEATURES], train[TARGET].astype(int))
        probability = model.predict_proba(test[FEATURES])[:, 1]

        test = test.copy()
        test["probability"] = probability
        test["fold"] = fold["name"]

        fold_capacity = [
            concentration(
                test[TARGET].astype(int),
                probability,
                fraction,
            )
            for fraction in (0.05, 0.10, 0.20)
        ]

        top_count = max(1, int(math.ceil(len(test) * 0.10)))
        top_index = np.argsort(-probability)[:top_count]
        model_top = np.zeros(len(test), dtype=bool)
        model_top[top_index] = True
        rule_priority = test["rule_score"].to_numpy() >= 2

        fold_diagnostics.append({
            "name": fold["name"],
            "test_rows": int(len(test)),
            "test_positive_rate": float(test[TARGET].mean()),
            "capacity": fold_capacity,
            "top_10_overlap": {
                "model_top_10_rows": int(model_top.sum()),
                "rule_high_or_critical_rows": int(rule_priority.sum()),
                "overlap_rows": int((model_top & rule_priority).sum()),
                "share_model_top_10_also_rule_priority": float(
                    (model_top & rule_priority).sum()
                    / model_top.sum()
                ),
                "model_only_rows": int(
                    (model_top & ~rule_priority).sum()
                ),
                "rule_only_rows": int(
                    (~model_top & rule_priority).sum()
                ),
            },
        })

        pooled.append(
            test[
                [
                    "provider_id",
                    "month",
                    "provider_type",
                    "region",
                    TARGET,
                    "rule_score",
                    "probability",
                    "fold",
                ]
            ]
        )

    pooled_frame = pd.concat(pooled, ignore_index=True)

    pooled_capacity = [
        concentration(
            pooled_frame[TARGET].astype(int),
            pooled_frame["probability"].to_numpy(),
            fraction,
        )
        for fraction in (0.05, 0.10, 0.20)
    ]

    result = {
        "model": "regularized logistic regression",
        "target": TARGET,
        "out_of_time_rows": int(len(pooled_frame)),
        "out_of_time_positives": int(pooled_frame[TARGET].sum()),
        "out_of_time_prevalence": float(
            pooled_frame[TARGET].mean()
        ),
        "pooled_metrics": metrics(
            pooled_frame[TARGET].astype(int),
            pooled_frame["probability"].to_numpy(),
        ),
        "pooled_capacity": pooled_capacity,
        "calibration": calibration_summary(pooled_frame),
        "segments": {
            "provider_type": segment_metrics(
                pooled_frame,
                "provider_type",
            ),
            "region": segment_metrics(
                pooled_frame,
                "region",
            ),
        },
        "fold_diagnostics": fold_diagnostics,
        "coefficient_review": fit_latest_coefficients(frame),
    }

    METADATA.mkdir(parents=True, exist_ok=True)
    (METADATA / "model_diagnostics.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
