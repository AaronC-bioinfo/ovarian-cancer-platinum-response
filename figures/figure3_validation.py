"""
figure3_validation.py
─────────────────────
Figure 3: External validation AUC on GSE63885.

Two-panel figure:
  Left:  Clinical label (CR/PR vs P/SD)
  Right: DFS label (sensitive vs resistant)

Each panel is a heatmap of AUC values (model × OS-threshold), with a
dashed 0.5 chance-level reference and colour scale anchored at 0.5.

Usage:
    python figures/figure3_validation.py \
        --results results/external_validation_results.csv \
        --out     figures/figure3_validation.png

Outputs:
    figures/figure3_validation.png  (300 dpi, publication-ready)
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

GREY       = "#555555"
LIGHT_GREY = "#DDDDDD"

MODEL_ORDER     = ["Logistic Regression", "Random Forest", "SVM (RBF)"]
THRESHOLD_ORDER = ["12m", "18m", "24m"]

LABEL_TITLES = {
    "clinical": "Clinical label\n(CR/PR = responder vs P/SD = non-responder)",
    "dfs":      "DFS label\n(sensitive vs resistant)",
}

# Diverging colormap centred at 0.5 (chance level)
# Blue = below chance, white = chance, red = above chance
CMAP = mcolors.LinearSegmentedColormap.from_list(
    "auc_diverge",
    [(0.0, "#2166AC"), (0.5, "#F7F7F7"), (1.0, "#D6604D")],
)


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df


def pivot_label(df: pd.DataFrame, label: str) -> pd.DataFrame:
    sub = df[df["label_set"] == label].copy()
    sub["threshold"] = sub["threshold"].str.strip()
    pivot = sub.pivot(index="model", columns="threshold", values="auc")
    pivot = pivot.loc[MODEL_ORDER, THRESHOLD_ORDER]
    return pivot


def make_figure(df: pd.DataFrame, out_path: Path):
    fig, axes = plt.subplots(
        1, 2,
        figsize=(10, 3.8),
        gridspec_kw={"wspace": 0.35},
    )
    fig.patch.set_facecolor("white")

    for ax, label in zip(axes, ["clinical", "dfs"]):
        pivot = pivot_label(df, label)
        data  = pivot.values.astype(float)

        # Heatmap
        im = ax.imshow(
            data,
            cmap=CMAP,
            vmin=0.3, vmax=0.7,   # anchored: 0.5 is chance
            aspect="auto",
        )

        # Annotate each cell with AUC value
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                val = data[i, j]
                # Dark text on light cells, light text on dark cells
                brightness = abs(val - 0.5)
                txt_col = "white" if brightness > 0.12 else GREY
                ax.text(
                    j, i, f"{val:.3f}",
                    ha="center", va="center",
                    fontsize=11, fontweight="bold",
                    color=txt_col,
                )

        # Axes formatting
        ax.set_xticks(range(len(THRESHOLD_ORDER)))
        ax.set_xticklabels(THRESHOLD_ORDER, fontsize=10)
        ax.set_yticks(range(len(MODEL_ORDER)))
        ax.set_yticklabels(
            ["LR", "RF", "SVM"],
            fontsize=10, fontweight="bold",
        )
        ax.set_xlabel("OS threshold used to train TCGA classifier",
                      fontsize=9, color=GREY, labelpad=6)
        ax.set_title(LABEL_TITLES[label],
                     fontsize=10, fontweight="bold", color=GREY, pad=10)

        # Chance-level border highlight on cells near 0.5
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if abs(data[i, j] - 0.5) < 0.03:
                    rect = plt.Rectangle(
                        (j - 0.5, i - 0.5), 1, 1,
                        fill=False, edgecolor=GREY,
                        linewidth=1.5, linestyle="--",
                    )
                    ax.add_patch(rect)

        # Colourbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.82, pad=0.03)
        cbar.set_label("AUC", fontsize=9, color=GREY)
        cbar.ax.tick_params(labelsize=8)
        cbar.ax.axhline(
            (0.5 - 0.3) / (0.7 - 0.3),   # normalised position of 0.5
            color=GREY, linewidth=1.2, linestyle="--",
        )
        cbar.ax.text(
            2.5, (0.5 - 0.3) / (0.7 - 0.3),
            "chance", fontsize=7, color=GREY, va="center",
        )

        ax.spines[:].set_visible(False)
        ax.tick_params(length=0)

    fig.suptitle(
        "Figure 3. Classifiers trained on TCGA RNA-seq do not generalise to GSE63885 microarray cohort\n"
        "All AUC values cluster near chance (0.5) regardless of model or label set  "
        "(dashed outlines = AUC within ±0.03 of chance)",
        fontsize=9.5, y=1.06, color=GREY,
    )

    plt.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Figure 3 — external validation heatmap")
    parser.add_argument("--results", default="results/external_validation_results.csv")
    parser.add_argument("--out",     default="figures/figure3_validation.png")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = load_data(Path(args.results))
    make_figure(df, out_path)


if __name__ == "__main__":
    main()
