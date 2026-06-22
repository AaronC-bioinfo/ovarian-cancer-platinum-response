"""
test_ablation.py
─────────────────
Unit tests for ablation.py — uses synthetic data so these tests run without
needing the real TCGA dataset on disk.

Run with: pytest tests/ -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ablation import (
    bootstrap_auc_ci,
    nested_cross_validate,
    _select_top_f_score,
    _select_top_variance,
)
from src.ablation import test_leakage_significance as check_leakage_significance


# ─────────────────────────────────────────────────────────────────────────────
# bootstrap_auc_ci
# ─────────────────────────────────────────────────────────────────────────────


class TestBootstrapAucCi:
    @pytest.fixture
    def perfect_classifier_data(self):
        rng = np.random.RandomState(0)
        y_true = np.array([0] * 50 + [1] * 50)
        # Perfect separation: class 1 always has higher score
        y_prob = np.concatenate([rng.uniform(0, 0.4, 50), rng.uniform(0.6, 1.0, 50)])
        return y_true, y_prob

    @pytest.fixture
    def random_classifier_data(self):
        rng = np.random.RandomState(0)
        y_true = rng.randint(0, 2, 200)
        y_prob = rng.uniform(0, 1, 200)  # uninformative scores
        return y_true, y_prob

    def test_point_estimate_near_one_for_good_classifier(self, perfect_classifier_data):
        y_true, y_prob = perfect_classifier_data
        result = bootstrap_auc_ci(y_true, y_prob, n_bootstrap=200, seed=1)
        assert result["point_estimate"] > 0.95

    def test_ci_bounds_are_ordered(self, perfect_classifier_data):
        y_true, y_prob = perfect_classifier_data
        result = bootstrap_auc_ci(y_true, y_prob, n_bootstrap=200, seed=1)
        assert result["ci_lower"] <= result["point_estimate"] <= result["ci_upper"]

    def test_random_classifier_ci_contains_point_five(self, random_classifier_data):
        y_true, y_prob = random_classifier_data
        result = bootstrap_auc_ci(y_true, y_prob, n_bootstrap=500, seed=1)
        # A near-random classifier's CI should plausibly span 0.5
        assert result["ci_lower"] < 0.6

    def test_returns_expected_keys(self, perfect_classifier_data):
        y_true, y_prob = perfect_classifier_data
        result = bootstrap_auc_ci(y_true, y_prob, n_bootstrap=50, seed=1)
        expected_keys = {"point_estimate", "ci_lower", "ci_upper", "std", "n_valid_bootstraps"}
        assert expected_keys.issubset(result.keys())

    def test_narrower_ci_with_more_data(self):
        # Larger n should generally produce a tighter CI than smaller n
        rng = np.random.RandomState(0)

        y_small = rng.randint(0, 2, 30)
        p_small = rng.uniform(0, 1, 30)
        small_result = bootstrap_auc_ci(y_small, p_small, n_bootstrap=300, seed=2)

        y_large = rng.randint(0, 2, 500)
        p_large = rng.uniform(0, 1, 500)
        large_result = bootstrap_auc_ci(y_large, p_large, n_bootstrap=300, seed=2)

        small_width = small_result["ci_upper"] - small_result["ci_lower"]
        large_width = large_result["ci_upper"] - large_result["ci_lower"]
        assert large_width < small_width


# ─────────────────────────────────────────────────────────────────────────────
# _select_top_variance
# ─────────────────────────────────────────────────────────────────────────────


class TestSelectTopVariance:
    def test_selects_highest_variance_columns(self):
        X = pd.DataFrame(
            {
                "low_var": [1, 1, 1, 1, 2],
                "high_var": [1, 100, 1, 100, 1],
                "mid_var": [1, 5, 1, 5, 1],
            }
        )
        top = _select_top_variance(X, top_n=1)
        assert list(top) == ["high_var"]

    def test_top_n_respected(self):
        X = pd.DataFrame(np.random.RandomState(0).rand(10, 20))
        top = _select_top_variance(X, top_n=5)
        assert len(top) == 5


# ─────────────────────────────────────────────────────────────────────────────
# _select_top_f_score
# ─────────────────────────────────────────────────────────────────────────────


class TestSelectTopFScore:
    def test_selects_label_correlated_columns(self):
        rng = np.random.RandomState(0)
        n = 100
        y = np.array([0] * 50 + [1] * 50)
        # informative: clearly separates the two classes
        informative = np.concatenate([rng.normal(0, 1, 50), rng.normal(5, 1, 50)])
        # noise: no relationship to y
        noise = rng.normal(0, 1, n)
        X = pd.DataFrame({"informative_gene": informative, "noise_gene": noise})

        top = _select_top_f_score(X, y, top_n=1)
        assert list(top) == ["informative_gene"]

    def test_top_n_respected(self):
        rng = np.random.RandomState(0)
        X = pd.DataFrame(rng.rand(50, 15), columns=[f"g{i}" for i in range(15)])
        y = rng.randint(0, 2, 50)
        top = _select_top_f_score(X, y, top_n=5)
        assert len(top) == 5

    def test_handles_constant_column_without_crashing(self):
        # A zero-variance column produces NaN F-score — should not crash
        rng = np.random.RandomState(0)
        X = pd.DataFrame(
            {
                "constant": [1.0] * 40,
                "varying": rng.rand(40),
            }
        )
        y = rng.randint(0, 2, 40)
        top = _select_top_f_score(X, y, top_n=1)
        assert list(top) == ["varying"]

    def test_handles_nan_values_without_crashing(self):
        # Regression test: real RSEM expression data contains NaN values
        # (missing measurements for some genes/samples) which sklearn's
        # f_classif cannot handle natively. This bug surfaced only on
        # real TCGA data, not in clean synthetic fixtures, until fixed.
        rng = np.random.RandomState(0)
        n = 60
        y = np.array([0] * 30 + [1] * 30)
        informative = np.concatenate([rng.normal(0, 1, 30), rng.normal(5, 1, 30)])
        noise = rng.normal(0, 1, n)

        X = pd.DataFrame({"informative_gene": informative, "noisy_gene_with_nans": noise})
        # Inject NaNs into a handful of entries, as real RSEM data has
        nan_idx = rng.choice(n, size=10, replace=False)
        X.loc[nan_idx, "noisy_gene_with_nans"] = np.nan

        # Should not raise, and should still correctly rank the informative gene first
        top = _select_top_f_score(X, y, top_n=1)
        assert list(top) == ["informative_gene"]

    def test_handles_all_nan_column_without_crashing(self):
        rng = np.random.RandomState(0)
        X = pd.DataFrame(
            {
                "all_nan": [np.nan] * 40,
                "varying": rng.rand(40),
            }
        )
        y = rng.randint(0, 2, 40)
        top = _select_top_f_score(X, y, top_n=1)
        assert list(top) == ["varying"]


# ─────────────────────────────────────────────────────────────────────────────
# test_leakage_significance
# ─────────────────────────────────────────────────────────────────────────────


class TestLeakageSignificance:
    @pytest.fixture
    def no_effect_ablation_df(self):
        # Leaky and correct AUCs drawn from the SAME distribution → expect
        # a non-significant result (this mirrors what we'd expect for
        # unsupervised variance selection).
        rng = np.random.RandomState(0)
        rows = []
        for seed in range(30):
            shared_auc_a = rng.normal(0.70, 0.03)
            shared_auc_b = rng.normal(0.70, 0.03)
            rows.append({"threshold_m": 12, "model": "LR", "condition": "leaky_condition", "auc": shared_auc_a, "seed": seed})
            rows.append({"threshold_m": 12, "model": "LR", "condition": "correct_condition", "auc": shared_auc_b, "seed": seed})
        return pd.DataFrame(rows)

    @pytest.fixture
    def strong_effect_ablation_df(self):
        # Leaky consistently higher than correct by a large, consistent margin
        rng = np.random.RandomState(0)
        rows = []
        for seed in range(30):
            base = rng.normal(0.65, 0.02)
            rows.append({"threshold_m": 12, "model": "LR", "condition": "leaky_condition", "auc": base + 0.15, "seed": seed})
            rows.append({"threshold_m": 12, "model": "LR", "condition": "correct_condition", "auc": base, "seed": seed})
        return pd.DataFrame(rows)

    def test_returns_expected_columns(self, no_effect_ablation_df):
        result = check_leakage_significance(no_effect_ablation_df)
        expected = {"threshold_m", "model", "mean_inflation", "wilcoxon_p", "ttest_p", "n_pairs", "significant_at_05"}
        assert expected.issubset(result.columns)

    def test_strong_effect_is_significant(self, strong_effect_ablation_df):
        result = check_leakage_significance(strong_effect_ablation_df)
        row = result.iloc[0]
        assert bool(row["significant_at_05"]) is True
        # mean_inflation = leaky − correct, and leaky was constructed +0.15 higher
        assert row["mean_inflation"] > 0.1

    def test_rejects_more_than_two_conditions(self):
        df = pd.DataFrame(
            {
                "threshold_m": [12, 12, 12],
                "model": ["LR", "LR", "LR"],
                "condition": ["a", "b", "c"],
                "auc": [0.7, 0.7, 0.7],
                "seed": [0, 0, 0],
            }
        )
        with pytest.raises(ValueError):
            check_leakage_significance(df)

    def test_n_pairs_matches_seed_count(self, no_effect_ablation_df):
        result = check_leakage_significance(no_effect_ablation_df)
        assert result.iloc[0]["n_pairs"] == 30


# ─────────────────────────────────────────────────────────────────────────────
# nested_cross_validate (synthetic classification task)
# ─────────────────────────────────────────────────────────────────────────────


class TestNestedCrossValidate:
    @pytest.fixture
    def synthetic_data(self):
        X, y = make_classification(
            n_samples=120,
            n_features=30,
            n_informative=8,
            n_redundant=2,
            class_sep=1.2,
            random_state=42,
        )
        X_df = pd.DataFrame(X, columns=[f"gene_{i}" for i in range(30)])
        return X_df, y

    def test_returns_expected_keys(self, synthetic_data):
        X, y = synthetic_data

        def selector(X_train, X_test):
            top = _select_top_variance(X_train, top_n=10)
            return X_train[top], X_test[top]

        result = nested_cross_validate(
            model_builder=lambda: LogisticRegression(max_iter=1000),
            X=X,
            y=y,
            feature_selector=selector,
            outer_splits=4,
            seed=0,
        )
        assert {"mean_auc", "std_auc", "fold_aucs"}.issubset(result.keys())
        assert len(result["fold_aucs"]) == 4

    def test_separable_data_yields_good_auc(self, synthetic_data):
        X, y = synthetic_data

        def selector(X_train, X_test):
            top = _select_top_variance(X_train, top_n=15)
            return X_train[top], X_test[top]

        result = nested_cross_validate(
            model_builder=lambda: LogisticRegression(max_iter=1000),
            X=X,
            y=y,
            feature_selector=selector,
            outer_splits=4,
            seed=0,
        )
        # Well-separated synthetic data should yield a clearly-better-than-random AUC
        assert result["mean_auc"] > 0.65

    def test_fold_auc_count_matches_splits(self, synthetic_data):
        X, y = synthetic_data

        def selector(X_train, X_test):
            return X_train, X_test  # no-op selection

        result = nested_cross_validate(
            model_builder=lambda: LogisticRegression(max_iter=1000),
            X=X,
            y=y,
            feature_selector=selector,
            outer_splits=5,
            seed=1,
        )
        assert len(result["fold_aucs"]) == 5
