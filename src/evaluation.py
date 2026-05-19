"""
evaluation.py
─────────────
Unified metrics computation for all models and thresholds.

Returns structured results (dicts / DataFrames) so that downstream
reporting and visualisation code can consume them without re-running
inference.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Single model evaluation
# ─────────────────────────────────────────────────────────────────────────────


def evaluate_model(
    model: Any,
    X_test: np.ndarray,
    y_test: np.ndarray,
    model_name: str = "",
) -> dict:
    """
    Compute a standard suite of classification metrics for one model.

    Args:
        model:      Fitted sklearn estimator.
        X_test:     Test feature matrix.
        y_test:     True labels.
        model_name: Label used in logging.

    Returns:
        Dict containing:
            ``roc_auc``, ``accuracy``, ``confusion_matrix``,
            ``classification_report``, ``y_pred``, ``y_prob``.
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model_name": model_name,
        "roc_auc": roc_auc_score(y_test, y_prob),
        "accuracy": accuracy_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(
            y_test, y_pred, zero_division=0, output_dict=True
        ),
        "y_pred": y_pred,
        "y_prob": y_prob,
    }

    logger.info(
        "%s → ROC-AUC: %.3f | Accuracy: %.3f",
        model_name or type(model).__name__,
        metrics["roc_auc"],
        metrics["accuracy"],
    )
    return metrics


# ─────────────────────────────────────────────────────────────────────────────
# Multi-model / multi-threshold evaluation
# ─────────────────────────────────────────────────────────────────────────────


def evaluate_all_models(
    trained_models: dict[str, Any],
    X_test: np.ndarray,
    y_test: np.ndarray,
    threshold: int,
) -> list[dict]:
    """
    Evaluate all trained models for a single threshold.

    Args:
        trained_models: Dict mapping model name → fitted estimator.
        X_test:         Test feature matrix.
        y_test:         True labels.
        threshold:      The survival threshold (months) — used only for logging.

    Returns:
        List of metric dicts (one per model).
    """
    results = []
    for name, model in trained_models.items():
        metrics = evaluate_model(model, X_test, y_test, model_name=f"{name} ({threshold}m)")
        metrics["threshold"] = threshold
        results.append(metrics)
    return results


def build_results_table(all_results: list[dict]) -> pd.DataFrame:
    """
    Flatten a list of metric dicts into a tidy summary DataFrame.

    Args:
        all_results: Concatenated output of :func:`evaluate_all_models`
                     across all thresholds.

    Returns:
        DataFrame with columns [model_name, threshold, roc_auc, accuracy,
        precision, recall, f1_score].
    """
    rows = []
    for r in all_results:
        report = r["classification_report"]
        rows.append(
            {
                "model": r["model_name"],
                "threshold_m": r["threshold"],
                "roc_auc": round(r["roc_auc"], 4),
                "accuracy": round(r["accuracy"], 4),
                "precision_class1": round(report.get("1", {}).get("precision", np.nan), 4),
                "recall_class1": round(report.get("1", {}).get("recall", np.nan), 4),
                "f1_class1": round(report.get("1", {}).get("f1-score", np.nan), 4),
            }
        )

    return pd.DataFrame(rows).sort_values(["threshold_m", "roc_auc"], ascending=[True, False])
