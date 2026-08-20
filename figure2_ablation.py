"""
figure2_ablation.py
───────────────────
Figure 2: Feature selection leakage ablation results.

Grouped bar chart comparing clean vs. leaky AUC for supervised F-score
selection across all 9 model × threshold combinations, with the
unsupervised variance (clean) baseline overlaid as a reference line.

Usage:
    python figures/figure2_ablation.py \
        --supervised results/ablation_supervised_leakage_summary.csv \
        --variance   results/ablation_split_variance_summary.csv \
        --out        figures/figure2_ablation.png

Outputs:
    figures/figure2_ablation.png  (300 dpi, publication-ready)
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ── Colour palette (colourblind-safe) ────────────────────────────────────────
CLEAN_COL  = "#2166AC"   # blue  — clean / correct
LEAKY_COL  = "#D6604D"   # red   — leaky / inflated
VAR_COL    = "#4DAC26"   # green — unsupervised variance baseline
GREY       = "#555555"
LIGHT_GREY = "#DDDDDD"

MODEL_LABELS = {
    "Logistic Regression": "LR",
    "Random Forest":        "RF",
    "SVM":                  "SVM",
}
THRESHOLDS = [12, 18, 24]
MODELS     = ["Logistic Regression", "Random Forest", "SVM"]


def load_data(sup_path: Path, var_path: Path):
    sup = pd.read_csv(sup_path)
    var = pd.read_csv(var_path)
    return sup, var


def build_arrays(sup: pd.DataFrame, var: pd.DataFrame):
    """
    Returns dicts keyed by threshold → array of length 3 (one per model).
    """
    clean, leaky, variance = {}, {}, {}
    for thr in THRESHOLDS:
        clean[thr]    = []
        leaky[thr]    = []
        variance[thr] = []
        for model in MODELS:
            s_row = sup[(sup.threshold_m == thr) & (sup.model == model)]
            v_row = var[(var.threshold_m == thr) & (var.model == model)]
            clean[thr].append(
                float(s_row["mean_supervised_correct_train_only_fscore"].iloc[0])
            )
            leaky[thr].append(
                float(s_row["mean_supervised_leaky_full_data_fscore"].iloc[0])
            )
            variance[thr].append(float(v_row["mean"].iloc[0]))
    return clean, leaky, variance


def make_figure(clean, leaky, variance, out_path: Path):
    n_models = len(MODELS)
    n_thr    = len(THRESHOLDS)

    # Layout: 1 row × 3 columns, one panel per threshold
    fig, axes = plt.subplots(
        1, 3,
        figsize=(13, 4.8),
        sharey=True,
        gridspec_kw={"wspace": 0.08},
    )
    fig.patch.set_facecolor("white")

    bar_w  = 0.28
    x      = np.arange(n_models)
    offsets = [-bar_w, 0, bar_w]   # variance baseline, clean, leaky

    for ax, thr in zip(axes, THRESHOLDS):
        ax.set_facecolor("white")

        v_vals = variance[thr]
        c_vals = clean[thr]
        l_vals = leaky[thr]

        # Unsupervised variance bars (reference)
        ax.bar(x + offsets[0], v_vals, bar_w,
               color=VAR_COL, alpha=0.75, zorder=3, label="Unsupervised (variance)")

        # Clean supervised bars
        ax.bar(x + offsets[1], c_vals, bar_w,
               color=CLEAN_COL, alpha=0.85, zorder=3, label="Supervised — clean")

        # Leaky supervised bars
        bars = ax.bar(x + offsets[2], l_vals, bar_w,
                      color=LEAKY_COL, alpha=0.85, zorder=3, label="Supervised — leaky")

        # Inflation annotations above leaky bars
        for xi, (c, l) in enumerate(zip(c_vals, l_vals)):
            inflation = l - c
            if abs(inflation) >= 0.02:
                sign = "+" if inflation >= 0 else ""
                ax.text(
                    xi + offsets[2], l + 0.012,
                    f"{sign}{inflation:.2f}",
                    ha="center", va="bottom",
                    fontsize=7.5, color=LEAKY_COL, fontweight="bold",
                )

        # Chance line
        ax.axhline(0.5, color=GREY, linewidth=0.9, linestyle="--",
                   zorder=2, alpha=0.7)
        ax.text(n_models - 0.45, 0.502, "Chance", fontsize=7,
                color=GREY, va="bottom")

        # Panel formatting
        ax.set_xlim(-0.55, n_models - 0.45)
        ax.set_ylim(0, 1.10)
        ax.set_xticks(x)
        ax.set_xticklabels([MODEL_LABELS[m] for m in MODELS],
                           fontsize=10, fontweight="bold")
        ax.set_title(f"{thr}-month threshold",
                     fontsize=11, fontweight="bold", pad=8, color=GREY)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(LIGHT_GREY)
        ax.tick_params(axis="both", which="both", length=0)
        ax.yaxis.set_tick_params(labelsize=9)
        ax.grid(axis="y", color=LIGHT_GREY, linewidth=0.6, zorder=1)

    axes[0].set_ylabel("Mean AUC (30 repeated splits)", fontsize=10, color=GREY)

    # Shared legend
    handles = [
        mpatches.Patch(color=VAR_COL,   alpha=0.75, label="Unsupervised (variance) — clean"),
        mpatches.Patch(color=CLEAN_COL, alpha=0.85, label="Supervised (F-score) — clean"),
        mpatches.Patch(color=LEAKY_COL, alpha=0.85, label="Supervised (F-score) — leaky"),
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=3,
        fontsize=9,
        frameon=False,
    )

    fig.suptitle(
        "Figure 2. Feature selection leakage inflates reported AUC\n"
        "Red annotations show AUC inflation (leaky − clean) for supervised F-score selection",
        fontsize=10, y=1.10, color=GREY,
    )

    plt.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Figure 2 — ablation leakage chart")
    parser.add_argument("--supervised", default="results/ablation_supervised_leakage_summary.csv")
    parser.add_argument("--variance",   default="results/ablation_split_variance_summary.csv")
    parser.add_argument("--out",        default="figures/figure2_ablation.png")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sup, var = load_data(Path(args.supervised), Path(args.variance))
    clean, leaky, variance = build_arrays(sup, var)
    make_figure(clean, leaky, variance, out_path)


if __name__ == "__main__":
    main()
