"""
models.py
─────────
Model definitions, training, cross-validation and persistence.

All classifiers use ``class_weight='balanced'`` by default to handle
the class imbalance inherent in the platinum-response labelling scheme.
"""

from __future__ import annotations

import logging
import pickle
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.svm import SVC

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Factory helpers
# ─────────────────────────────────────────────────────────────────────────────

ModelConfig = dict[str, Any]


def build_logistic_regression(cfg: ModelConfig) -> LogisticRegression:
    return LogisticRegression(
        max_iter=cfg.get("max_iter", 5000),
        penalty=cfg.get("penalty", "l2"),
        class_weight=cfg.get("class_weight", "balanced"),
        random_state=cfg.get("seed", 42),
    )


def build_random_forest(cfg: ModelConfig) -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=cfg.get("n_estimators", 300),
        max_depth=cfg.get("max_depth", None),
        min_samples_split=cfg.get("min_samples_split", 2),
        class_weight=cfg.get("class_weight", "balanced"),
        n_jobs=-1,
        random_state=cfg.get("seed", 42),
    )


def build_svm(cfg: ModelConfig) -> SVC:
    return SVC(
        kernel=cfg.get("kernel", "rbf"),
        C=cfg.get("C", 1),
        gamma=cfg.get("gamma", "scale"),
        probability=True,
        class_weight=cfg.get("class_weight", "balanced"),
        random_state=cfg.get("seed", 42),
    )


def get_all_models(full_cfg: dict) -> dict[str, Any]:
    """
    Instantiate all three classifiers from the project configuration.

    Args:
        full_cfg: Top-level config dict (loaded from config.yaml).

    Returns:
        Dict mapping model name → sklearn estimator instance.
    """
    seed = full_cfg["project"]["seed"]
    model_cfg = full_cfg["model"]

    lr_cfg = {**model_cfg["logistic_regression"], "seed": seed}
    rf_cfg = {**model_cfg["random_forest"], "seed": seed}
    svm_cfg = {**model_cfg["svm"], "seed": seed}

    return {
        "Logistic Regression": build_logistic_regression(lr_cfg),
        "Random Forest": build_random_forest(rf_cfg),
        "SVM": build_svm(svm_cfg),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Training & evaluation helpers
# ─────────────────────────────────────────────────────────────────────────────


def train_model(model: Any, X_train: np.ndarray, y_train: np.ndarray) -> Any:
    """Fit a model and log a brief summary."""
    model_name = type(model).__name__
    logger.info("Training %s …", model_name)
    model.fit(X_train, y_train)
    logger.info("%s training complete.", model_name)
    return model


def cross_validate_model(
    model: Any,
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    seed: int = 42,
) -> dict[str, float]:
    """
    Compute stratified k-fold cross-validation ROC-AUC scores.

    Args:
        model:    A fitted or unfitted sklearn estimator.
        X:        Feature matrix (training set recommended).
        y:        Label array.
        n_splits: Number of CV folds.
        seed:     Random seed for fold shuffling.

    Returns:
        Dict with keys ``mean``, ``std``, ``scores`` (raw array).
    """
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    result = {"mean": float(scores.mean()), "std": float(scores.std()), "scores": scores}
    logger.info(
        "%s CV ROC-AUC: %.3f ± %.3f",
        type(model).__name__,
        result["mean"],
        result["std"],
    )
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Persistence
# ─────────────────────────────────────────────────────────────────────────────


def save_model(model: Any, path: str | Path) -> None:
    """Serialise a model to disk using pickle."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)
    logger.info("Model saved → %s", path)


def load_model(path: str | Path) -> Any:
    """Deserialise a model from disk."""
    with open(path, "rb") as f:
        model = pickle.load(f)
    logger.info("Model loaded ← %s", path)
    return model
