"""
figure1_pipeline.py
───────────────────
Figure 1: Software pipeline architecture diagram.

A schematic showing the flow from raw TCGA data inputs through the
seven source modules to outputs (AUC results, ablation findings,
label investigation). Uses only matplotlib — no external diagram
libraries required.

Usage:
    python figures/figure1_pipeline.py \
        --out figures/figure1_pipeline.png

Outputs:
    figures/figure1_pipeline.png  (300 dpi, publication-ready)
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ── Colour scheme ─────────────────────────────────────────────────────────────
C_INPUT   = "#D6EAF8"   # light blue  — inputs
C_CORE    = "#2166AC"   # deep blue   — core pipeline modules
C_ANALYSE = "#1A5276"   # darker blue — analysis modules
C_OUTPUT  = "#EBF5FB"   # very light  — outputs
C_BORDER  = "#AED6F1"
C_TEXT    = "#1B2631"
C_GREY    = "#555555"
C_ARROW   = "#555555"
WHITE     = "#FFFFFF"


def box(ax, x, y, w, h, label, sublabel=None,
        facecolor=C_CORE, textcolor=WHITE, fontsize=9, bold=True):
    rect = mpatches.FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle="round,pad=0.02",
        facecolor=facecolor,
        edgecolor=C_BORDER,
        linewidth=1.2,
        zorder=3,
    )
    ax.add_patch(rect)
    weight = "bold" if bold else "normal"
    if sublabel:
        ax.text(x, y + 0.018, label, ha="center", va="center",
                fontsize=fontsize, color=textcolor, fontweight=weight, zorder=4)
        ax.text(x, y - 0.022, sublabel, ha="center", va="center",
                fontsize=fontsize - 1.5, color=textcolor, alpha=0.85,
                style="italic", zorder=4)
    else:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fontsize, color=textcolor, fontweight=weight, zorder=4)


def arrow(ax, x0, y0, x1, y1, style="->"):
    ax.annotate(
        "", xy=(x1, y1), xytext=(x0, y0),
        arrowprops=dict(
            arrowstyle=style,
            color=C_ARROW,
            lw=1.3,
            connectionstyle="arc3,rad=0.0",
        ),
        zorder=2,
    )


def make_figure(out_path: Path):
    fig, ax = plt.subplots(figsize=(13, 6.5))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # ── Column x positions ────────────────────────────────────────────────────
    X_IN   = 0.10   # inputs
    X_LOAD = 0.26   # data_loader + preprocessing
    X_FEAT = 0.44   # features
    X_MOD  = 0.60   # models
    X_EVAL = 0.76   # evaluation
    X_OUT  = 0.92   # outputs

    BW = 0.13   # box width
    BH = 0.08   # box height standard

    # ── INPUT FILES ───────────────────────────────────────────────────────────
    # Three input files stacked vertically
    input_y = [0.78, 0.60, 0.42]
    input_labels = [
        ("data_mrna_seq\n_v2_rsem.txt", "RNA-seq expression"),
        ("data_clinical\n_patient.txt", "OS / survival data"),
        ("data_timeline\n_treatment.txt", "Platinum filtering"),
    ]
    for y, (lbl, sub) in zip(input_y, input_labels):
        box(ax, X_IN, y, BW, BH, lbl, sub,
            facecolor=C_INPUT, textcolor=C_TEXT, fontsize=7.5)

    # ── YAML config box (below inputs) ───────────────────────────────────────
    box(ax, X_IN, 0.22, BW, 0.065, "config.yaml",
        "YAML configuration",
        facecolor="#FDFEFE", textcolor=C_GREY, fontsize=7.5, bold=False)

    # ── CORE MODULES ─────────────────────────────────────────────────────────
    # data_loader
    box(ax, X_LOAD, 0.78, BW, BH, "data_loader",
        "Load & filter cohort")
    # preprocessing
    box(ax, X_LOAD, 0.60, BW, BH, "preprocessing",
        "Labels + StandardScaler")
    # features
    box(ax, X_FEAT, 0.69, BW, BH, "features",
        "Variance / F-score\nselection (top 500)")

    # models
    box(ax, X_MOD, 0.69, BW, BH, "models",
        "LR · RF · SVM(RBF)")

    # evaluation
    box(ax, X_EVAL, 0.69, BW, BH, "evaluation",
        "AUC · CI · permutation")

    # ── ANALYSIS MODULES ─────────────────────────────────────────────────────
    box(ax, X_FEAT, 0.40, BW, BH, "ablation",
        "Leakage ablation\n30 repeated splits",
        facecolor=C_ANALYSE)
    box(ax, X_FEAT, 0.22, BW, BH, "label_\ninvestigation",
        "Construct validity\ncheck",
        facecolor=C_ANALYSE)

    # ── CLI ENTRY POINTS (right side of analysis modules) ────────────────────
    box(ax, X_MOD, 0.40, BW*0.85, 0.065, "run_ablation\n_study.py",
        facecolor="#EBF5FB", textcolor=C_GREY, fontsize=7.5, bold=False)
    box(ax, X_MOD, 0.22, BW*0.85, 0.065, "investigate_\nclinical_labels.py",
        facecolor="#EBF5FB", textcolor=C_GREY, fontsize=7.5, bold=False)
    box(ax, X_MOD, 0.90, BW*0.85, 0.065, "run.py",
        facecolor="#EBF5FB", textcolor=C_GREY, fontsize=7.5, bold=False)

    # ── OUTPUTS ───────────────────────────────────────────────────────────────
    out_y = [0.84, 0.69, 0.52, 0.36, 0.20]
    out_labels = [
        "model_performance\n_summary.csv",
        "ablation_supervised\n_leakage_*.csv",
        "ablation_split\n_variance_*.csv",
        "label_investigation\n_recall_*.csv",
        "external_validation\n_results.csv",
    ]
    for y, lbl in zip(out_y, out_labels):
        box(ax, X_OUT, y, BW, 0.072, lbl,
            facecolor=C_OUTPUT, textcolor=C_TEXT, fontsize=7, bold=False)

    # ── ARROWS: inputs → data_loader ─────────────────────────────────────────
    for y in input_y:
        arrow(ax, X_IN + BW/2, y, X_LOAD - BW/2, 0.78 if y == 0.78 else 0.60)

    # data_loader → preprocessing
    arrow(ax, X_LOAD, 0.78 - BH/2, X_LOAD, 0.60 + BH/2)

    # preprocessing → features (main pipeline)
    arrow(ax, X_LOAD + BW/2, 0.69, X_FEAT - BW/2, 0.69)

    # features → models
    arrow(ax, X_FEAT + BW/2, 0.69, X_MOD - BW/2, 0.69)

    # models → evaluation
    arrow(ax, X_MOD + BW/2, 0.69, X_EVAL - BW/2, 0.69)

    # preprocessing → ablation
    arrow(ax, X_LOAD + BW/2, 0.58, X_FEAT - BW/2, 0.40)

    # preprocessing → label_investigation
    arrow(ax, X_LOAD + BW/2, 0.56, X_FEAT - BW/2, 0.22)

    # ablation → CLI
    arrow(ax, X_FEAT + BW/2, 0.40, X_MOD - BW*0.85/2, 0.40)

    # label_investigation → CLI
    arrow(ax, X_FEAT + BW/2, 0.22, X_MOD - BW*0.85/2, 0.22)

    # evaluation → outputs (main)
    arrow(ax, X_EVAL + BW/2, 0.69, X_OUT - BW/2, 0.69)

    # ablation CLI → outputs
    arrow(ax, X_MOD + BW*0.85/2, 0.40, X_OUT - BW/2, 0.52)
    arrow(ax, X_MOD + BW*0.85/2, 0.40, X_OUT - BW/2, 0.36)

    # label CLI → outputs
    arrow(ax, X_MOD + BW*0.85/2, 0.22, X_OUT - BW/2, 0.20)

    # run.py → evaluation
    arrow(ax, X_MOD + BW*0.85/2, 0.90, X_EVAL, 0.69 + BH/2)

    # config → data_loader
    ax.annotate(
        "", xy=(X_LOAD - BW/2, 0.70), xytext=(X_IN + BW/2, 0.22 + 0.032),
        arrowprops=dict(
            arrowstyle="->", color=C_GREY, lw=0.9, linestyle="dashed",
            connectionstyle="arc3,rad=-0.25",
        ),
        zorder=2,
    )

    # evaluation → first output (model performance)
    arrow(ax, X_EVAL + BW/2, 0.74, X_OUT - BW/2, 0.84)

    # ── SECTION LABELS ────────────────────────────────────────────────────────
    label_style = dict(fontsize=8, color=C_GREY, ha="center",
                       style="italic", va="top")
    ax.text(X_IN,   0.96, "Data inputs",      **label_style)
    ax.text(X_LOAD, 0.96, "Loading &\npreprocessing", **label_style)
    ax.text(X_FEAT, 0.96, "Feature\nselection &\nanalysis", **label_style)
    ax.text(X_MOD,  0.96, "Models &\nCLI",    **label_style)
    ax.text(X_EVAL, 0.96, "Evaluation",        **label_style)
    ax.text(X_OUT,  0.96, "Outputs",           **label_style)

    # ── LEGEND ───────────────────────────────────────────────────────────────
    legend_items = [
        mpatches.Patch(facecolor=C_INPUT,   edgecolor=C_BORDER, label="Input data files"),
        mpatches.Patch(facecolor=C_CORE,    edgecolor=C_BORDER, label="Core pipeline modules"),
        mpatches.Patch(facecolor=C_ANALYSE, edgecolor=C_BORDER, label="Analysis modules"),
        mpatches.Patch(facecolor=C_OUTPUT,  edgecolor=C_BORDER, label="Output CSV files"),
        mpatches.Patch(facecolor="#EBF5FB", edgecolor=C_BORDER, label="CLI entry points"),
    ]
    ax.legend(
        handles=legend_items,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.04),
        ncol=5,
        fontsize=8,
        frameon=True,
        framealpha=0.9,
        edgecolor=C_BORDER,
    )

    ax.set_title(
        "Figure 1. Software pipeline architecture\n"
        "Modular Python package with 7 source modules, YAML-driven configuration, "
        "CLI entry points, and 52 unit tests",
        fontsize=10, color=C_GREY, pad=14,
    )

    plt.savefig(out_path, dpi=300, bbox_inches="tight",
                facecolor=WHITE, edgecolor="none")
    plt.close()
    print(f"Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate Figure 1 — pipeline architecture")
    parser.add_argument("--out", default="figures/figure1_pipeline.png")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    make_figure(out_path)


if __name__ == "__main__":
    main()
