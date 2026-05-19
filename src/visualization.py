"""
visualization.py
────────────────
Production-quality figures for the ovarian cancer platinum response project.

Design principles:
  - Every function is self-contained: pass in data, get a saved figure.
  - Consistent style via a shared ``apply_style()`` call.
  - All figures are saved at 300 DPI by default.
  - No global state modified.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.calibration import calibration_curve
from sklearn.metrics import ConfusionMatrixDisplay, roc_curve, auc

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Style
# ─────────────────────────────────────────────────────────────────────────────

PALETTE = {
    "Logistic Regression": "#2E86AB",
    "Random Forest": "#E84855",
    "SVM": "#3BB273",
    "baseline": "#555555",
}

TIMEPOINT_COLORS = {12: "#F4A261", 18: "#E76F51", 24: "#264653"}


def apply_style() -> None:
    """Apply a consistent, publication-ready matplotlib style."""
    sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
    plt.rcParams.update(
        {
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 120,
            "savefig.bbox": "tight",
        }
    )


apply_style()


def _save(fig: plt.Figure, path: Optional[str | Path], dpi: int = 300) -> None:
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        logger.info("Figure saved → %s", path)


# ─────────────────────────────────────────────────────────────────────────────
# Figure 1 — Class distribution
# ─────────────────────────────────────────────────────────────────────────────


def plot_class_distribution(
    label_dict: dict[int, pd.Series],
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Bar chart of class balance for each survival threshold.

    Args:
        label_dict: Dict mapping threshold (int) → label Series (0/1).
        save_path:  Optional file path to save the figure.
    """
    thresholds = sorted(label_dict.keys())
    n = len(thresholds)

    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4), sharey=True)
    axes = np.atleast_1d(axes)

    for ax, thr in zip(axes, thresholds):
        counts = pd.Series(label_dict[thr]).value_counts().sort_index()
        bars = ax.bar(
            ["Responder\n(0)", "Non-responder\n(1)"],
            counts.values,
            color=[TIMEPOINT_COLORS.get(thr, "#888888"), "#C94040"],
            width=0.55,
            edgecolor="white",
        )
        ax.bar_label(bars, fmt="%d", padding=4, fontsize=11, fontweight="bold")
        ax.set_title(f"{thr}-month endpoint", fontweight="bold")
        ax.set_ylabel("Number of patients")
        ax.set_ylim(0, max(counts.values) * 1.20)
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    fig.suptitle(
        "Platinum-response class balance across survival thresholds",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 2 — ROC curves
# ─────────────────────────────────────────────────────────────────────────────


def plot_roc_curves(
    y_test: np.ndarray,
    model_probs: dict[str, np.ndarray],
    title: str = "ROC Curves",
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Overlay ROC curves for multiple models on a single axes.

    Args:
        y_test:       True binary labels.
        model_probs:  Dict mapping model name → predicted probabilities.
        title:        Plot title.
        save_path:    Optional file path to save the figure.
    """
    fig, ax = plt.subplots(figsize=(6.5, 6))

    for name, probs in model_probs.items():
        fpr, tpr, _ = roc_curve(y_test, probs)
        area = auc(fpr, tpr)
        color = PALETTE.get(name, None)
        ax.plot(fpr, tpr, lw=2.0, color=color, label=f"{name}  (AUC = {area:.3f})")

    ax.plot([0, 1], [0, 1], "--", color=PALETTE["baseline"], lw=1.2, label="Random classifier")
    ax.fill_between([0, 1], [0, 1], alpha=0.04, color="grey")

    ax.set_xlabel("False Positive Rate", fontsize=12)
    ax.set_ylabel("True Positive Rate", fontsize=12)
    ax.set_title(title, fontsize=13, fontweight="bold")
    ax.legend(loc="lower right", frameon=True, framealpha=0.9)
    ax.set_xlim([-0.01, 1.01])
    ax.set_ylim([-0.01, 1.05])

    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 3 — Confusion matrices
# ─────────────────────────────────────────────────────────────────────────────


def plot_confusion_matrices(
    y_test: np.ndarray,
    model_preds: dict[str, np.ndarray],
    title: str = "Confusion Matrices",
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Side-by-side normalised confusion matrices for multiple models.

    Args:
        y_test:       True binary labels.
        model_preds:  Dict mapping model name → predicted labels.
        title:        Overall figure title.
        save_path:    Optional file path to save the figure.
    """
    n = len(model_preds)
    fig, axes = plt.subplots(1, n, figsize=(4.5 * n, 4))
    axes = np.atleast_1d(axes)

    for ax, (name, preds) in zip(axes, model_preds.items()):
        ConfusionMatrixDisplay.from_predictions(
            y_test,
            preds,
            display_labels=["Responder", "Non-resp."],
            cmap="Blues",
            colorbar=False,
            ax=ax,
            normalize="true",
            values_format=".2f",
        )
        ax.set_title(name, fontweight="bold")
        ax.set_xlabel("Predicted label")
        ax.set_ylabel("True label")

    fig.suptitle(title, fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 4 — CV ROC-AUC heatmap (all models × all thresholds)
# ─────────────────────────────────────────────────────────────────────────────


def plot_cv_auc_heatmap(
    cv_results: dict[str, dict],
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Heatmap of mean cross-validated ROC-AUC across model × threshold.

    Args:
        cv_results: Nested dict {threshold → {model_name → {"mean": float, "std": float}}}.
        save_path:  Optional file path to save the figure.
    """
    thresholds = sorted(cv_results.keys())
    model_names = list(next(iter(cv_results.values())).keys())

    data = pd.DataFrame(
        {
            thr: {m: cv_results[thr][m]["mean"] for m in model_names}
            for thr in thresholds
        }
    )
    data.columns = [f"{t}m" for t in thresholds]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    sns.heatmap(
        data,
        annot=True,
        fmt=".3f",
        cmap="YlGnBu",
        vmin=0.4,
        vmax=0.9,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Mean CV ROC-AUC"},
        ax=ax,
    )
    ax.set_title("Cross-validated ROC-AUC by model and survival threshold", fontweight="bold")
    ax.set_ylabel("")
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 5 — Feature importance (Random Forest)
# ─────────────────────────────────────────────────────────────────────────────


def plot_feature_importance(
    feature_names: np.ndarray,
    importances: np.ndarray,
    top_n: int = 20,
    title: str = "Top Predictive Genes — Random Forest",
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Horizontal bar chart of the top-N gene importances from a Random Forest.

    Args:
        feature_names: Array of gene names.
        importances:   Array of feature importances (same length).
        top_n:         Number of genes to display.
        title:         Plot title.
        save_path:     Optional file path to save the figure.
    """
    idx = np.argsort(importances)[::-1][:top_n]
    genes = feature_names[idx][::-1]
    scores = importances[idx][::-1]

    fig, ax = plt.subplots(figsize=(7, top_n * 0.38 + 1))
    bars = ax.barh(genes, scores, color=PALETTE["Random Forest"], edgecolor="white")
    ax.bar_label(bars, fmt="%.4f", padding=3, fontsize=9)
    ax.set_xlabel("Mean decrease in impurity", fontsize=11)
    ax.set_title(title, fontweight="bold")
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 6 — Calibration curves
# ─────────────────────────────────────────────────────────────────────────────


def plot_calibration_curves(
    calibration_data: dict[str, tuple],
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Reliability diagram comparing model calibration across thresholds.

    Args:
        calibration_data: Dict mapping label → (y_test, y_prob).
        save_path:        Optional file path to save the figure.
    """
    fig, ax = plt.subplots(figsize=(6, 5.5))

    ax.plot([0, 1], [0, 1], "--", color="grey", lw=1.5, label="Perfect calibration")

    colors = list(TIMEPOINT_COLORS.values()) + ["#9B5DE5", "#F15BB5", "#00BBF9"]

    for (label, (y_test, y_prob)), color in zip(calibration_data.items(), colors):
        frac_pos, mean_pred = calibration_curve(y_test, y_prob, n_bins=10, strategy="quantile")
        ax.plot(mean_pred, frac_pos, marker="o", lw=2, color=color, label=label)

    ax.set_xlabel("Mean predicted probability", fontsize=12)
    ax.set_ylabel("Fraction of positives", fontsize=12)
    ax.set_title("Calibration curves — Random Forest", fontweight="bold")
    ax.legend(fontsize=9, frameon=True, framealpha=0.9)
    plt.tight_layout()
    _save(fig, save_path)
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Figure 7 — Kaplan–Meier survival curves
# ─────────────────────────────────────────────────────────────────────────────


def plot_kaplan_meier(
    surv_df: pd.DataFrame,
    title: str = "Kaplan–Meier: Predicted Risk Groups",
    save_path: Optional[str | Path] = None,
) -> plt.Figure:
    """
    Kaplan–Meier curves stratified by model-predicted risk class.

    Requires the ``lifelines`` library.

    Args:
        surv_df:  DataFrame with columns [pred_class, time, event].
        title:    Plot title.
        save_path: Optional file path to save the figure.
    """
    try:
        from lifelines import KaplanMeierFitter
        from lifelines.statistics import logrank_test
    except ImportError as exc:
        raise ImportError(
            "lifelines is required for Kaplan–Meier plots. "
            "Install it with: pip install lifelines"
        ) from exc

    fig, ax = plt.subplots(figsize=(8, 5.5))
    kmf = KaplanMeierFitter()

    group_styles = {
        0: {"label": "Predicted low-risk", "color": TIMEPOINT_COLORS[24]},
        1: {"label": "Predicted high-risk", "color": "#C94040"},
    }

    groups = {}
    for cls, style in group_styles.items():
        mask = surv_df["pred_class"] == cls
        groups[cls] = surv_df.loc[mask]
        kmf.fit(groups[cls]["time"], groups[cls]["event"], label=style["label"])
        kmf.plot_survival_function(ax=ax, ci_show=True, color=style["color"], lw=2.0)

    # Log-rank test annotation
    lr = logrank_test(
        groups[0]["time"], groups[1]["time"],
        groups[0]["event"], groups[1]["event"],
    )
    p_str = f"p = {lr.p_value:.3f}" if lr.p_value >= 0.001 else "p < 0.001"
    ax.text(0.98, 0.96, p_str, transform=ax.transAxes,
            ha="right", va="top", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="grey", alpha=0.8))

    ax.set_xlabel("Overall survival time (months)", fontsize=12)
    ax.set_ylabel("Survival probability", fontsize=12)
    ax.set_title(title, fontweight="bold")
    ax.set_ylim([-0.02, 1.05])
    plt.tight_layout()
    _save(fig, save_path)
    return fig
