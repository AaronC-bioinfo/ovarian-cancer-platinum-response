"""
features.py
───────────
Feature-selection and dimensionality reduction for gene expression data.

Design note
───────────
Variance-based filtering is computed exclusively on the **training split**
to prevent information leakage from the test set — a common mistake in
genomic ML pipelines.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def select_high_variance_genes(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    top_n: int = 500,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Retain the ``top_n`` most variable genes, ranked by training-set variance.

    Variance is computed **only on the training set** to avoid data leakage.
    The same gene list is then applied to the test set.

    Args:
        X_train: Training feature matrix (patients × genes).
        X_test:  Test feature matrix (patients × genes).
        top_n:   Number of genes to retain.

    Returns:
        (X_train_reduced, X_test_reduced) as DataFrames with ``top_n`` columns.
    """
    variance = X_train.var(axis=0)
    top_genes = variance.nlargest(top_n).index

    logger.info(
        "Gene selection: top %d / %d genes by training variance",
        top_n,
        X_train.shape[1],
    )
    return X_train[top_genes], X_test[top_genes]


def scale_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, StandardScaler]:
    """
    Standardise features using z-score normalisation (zero mean, unit variance).

    Fit on training data only; transform both splits.

    Args:
        X_train: Training feature matrix.
        X_test:  Test feature matrix.

    Returns:
        (X_train_scaled, X_test_scaled, fitted_scaler).
        The scaler is returned so it can be persisted for inference.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logger.info(
        "Features scaled: mean ≈ %.4f, std ≈ %.4f (training set)",
        X_train_scaled.mean(),
        X_train_scaled.std(),
    )
    return X_train_scaled, X_test_scaled, scaler
