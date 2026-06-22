#!/usr/bin/env python3
"""
run_ablation_study.py
──────────────────────
Standalone entry point for the methods-critique analysis.

This script answers one question with data, not assertion:
"How much does reported AUC inflate when feature selection leaks across
the train/test split, and how much does it vary purely from the choice
of random split?"

It reuses the existing data loading / preprocessing pipeline but does NOT
require any new data beyond what's already configured in config.yaml.

Usage:
    python run_ablation_study.py
    python run_ablation_study.py --n-repeats 50
    python run_ablation_study.py --thresholds 12 24
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Methods-critique ablation study")
    parser.add_argument("--config", default="config/config.yaml")
    parser.add_argument("--n-repeats", type=int, default=30,
                        help="Number of random train/test splits per condition (default: 30)")
    parser.add_argument("--thresholds", nargs="+", type=int, default=None,
                        help="Override which survival thresholds to test")
    parser.add_argument("--log-level", default="INFO")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    if args.thresholds:
        cfg["clinical"]["thresholds"] = args.thresholds

    from src.ablation import (
        bootstrap_auc_ci,
        run_leakage_ablation,
        run_split_variance_ablation,
        run_supervised_leakage_ablation,
        summarize_leakage_ablation,
        summarize_supervised_leakage_ablation,
        test_leakage_significance,
    )
    from src.data_loader import load_clinical, load_expression, load_treatment
    from src.preprocessing import (
        build_labelled_survival,
        clean_expression,
        extract_survival,
        identify_platinum_patients,
    )
    from src.visualization import plot_leakage_ablation

    results_dir = Path(cfg["output"]["results_dir"])
    fig_dir = Path(cfg["output"]["figures_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 60)
    logger.info("METHODS-CRITIQUE ABLATION STUDY")
    logger.info("=" * 60)

    # ── Load & preprocess (same as main pipeline) ────────────────────────
    try:
        clinical = load_clinical(cfg["data"]["data_dir"], cfg["data"]["clinical_file"])
        treatment = load_treatment(cfg["data"]["data_dir"], cfg["data"]["treatment_file"])
        expr_raw = load_expression(cfg["data"]["data_dir"], cfg["data"]["expression_file"])
    except FileNotFoundError as exc:
        logger.error(
            "Data file not found: %s\n"
            "This script reuses the same dataset as run.py — make sure "
            "config/config.yaml points to a valid data_dir.",
            exc,
        )
        sys.exit(1)

    surv = extract_survival(clinical, cfg["clinical"]["time_col"], cfg["clinical"]["status_col"])
    platinum_ids = identify_platinum_patients(treatment, cfg["clinical"]["platinum_drugs"])
    labelled_dict = build_labelled_survival(
        surv, platinum_ids, cfg["clinical"]["time_col"], cfg["clinical"]["thresholds"]
    )
    expr = clean_expression(expr_raw)

    # ── Ablation 1: leakage inflation (unsupervised variance selection) ───
    logger.info("Running UNSUPERVISED (variance) leakage ablation (%d repeats per condition)...", args.n_repeats)
    leakage_df = run_leakage_ablation(expr, labelled_dict, cfg, n_repeats=args.n_repeats)
    leakage_df.to_csv(results_dir / "ablation_leakage_raw.csv", index=False)

    summary = summarize_leakage_ablation(leakage_df)
    summary.to_csv(results_dir / "ablation_leakage_summary.csv", index=False)
    logger.info("\n%s", summary.to_string(index=False))

    mean_inflation = summary["auc_inflation"].mean()
    logger.info(
        "\n>>> Mean AUC inflation from UNSUPERVISED (variance) leakage: +%.4f <<<",
        mean_inflation,
    )

    # Significance test — is this inflation distinguishable from noise?
    leakage_df_renamed = leakage_df.copy()
    sig_results = test_leakage_significance(leakage_df_renamed)
    sig_results.to_csv(results_dir / "ablation_leakage_significance.csv", index=False)
    logger.info(
        "\nSignificance test (paired, per model/threshold):\n%s",
        sig_results.to_string(index=False),
    )
    logger.info(
        ">>> %d/%d model-threshold combinations significant at p<0.05 <<<",
        sig_results["significant_at_05"].sum(),
        len(sig_results),
    )

    plot_leakage_ablation(
        leakage_df,
        save_path=fig_dir / "fig8_leakage_ablation.png",
    )

    # ── Ablation 1b: leakage inflation (SUPERVISED F-score selection) ─────
    # Contrast condition: feature selection that DOES use the label is
    # expected to leak far more than unsupervised variance filtering.
    logger.info("Running SUPERVISED (F-score) leakage ablation (%d repeats per condition)...", args.n_repeats)
    supervised_df = run_supervised_leakage_ablation(expr, labelled_dict, cfg, n_repeats=args.n_repeats)
    supervised_df.to_csv(results_dir / "ablation_supervised_leakage_raw.csv", index=False)

    supervised_summary = summarize_supervised_leakage_ablation(supervised_df)
    supervised_summary.to_csv(results_dir / "ablation_supervised_leakage_summary.csv", index=False)
    logger.info("\n%s", supervised_summary.to_string(index=False))

    supervised_mean_inflation = supervised_summary["auc_inflation"].mean()
    logger.info(
        "\n>>> Mean AUC inflation from SUPERVISED (F-score) leakage: +%.4f <<<",
        supervised_mean_inflation,
    )

    supervised_sig_results = test_leakage_significance(supervised_df)
    supervised_sig_results.to_csv(results_dir / "ablation_supervised_leakage_significance.csv", index=False)
    logger.info(
        "\nSupervised significance test (paired, per model/threshold):\n%s",
        supervised_sig_results.to_string(index=False),
    )

    plot_leakage_ablation(
        supervised_df,
        title="AUC Inflation from SUPERVISED Feature-Selection Leakage (F-score)",
        save_path=fig_dir / "fig9_supervised_leakage_ablation.png",
    )

    logger.info("=" * 60)
    logger.info("HEADLINE COMPARISON:")
    logger.info("  Unsupervised (variance) leakage: +%.4f mean AUC inflation", mean_inflation)
    logger.info("  Supervised (F-score) leakage:    +%.4f mean AUC inflation", supervised_mean_inflation)
    logger.info("=" * 60)

    # ── Ablation 2: split-variance (single split vs. repeated) ────────────
    logger.info("Running split-variance ablation...")
    split_df = run_split_variance_ablation(expr, labelled_dict, cfg, n_repeats=args.n_repeats)
    split_df.to_csv(results_dir / "ablation_split_variance_raw.csv", index=False)

    split_summary = (
        split_df.groupby(["threshold_m", "model"])["auc"]
        .agg(["mean", "std", "min", "max"])
        .round(4)
        .reset_index()
    )
    split_summary.to_csv(results_dir / "ablation_split_variance_summary.csv", index=False)
    logger.info("\nSplit-variance summary (range of AUC across %d random splits):", args.n_repeats)
    logger.info("\n%s", split_summary.to_string(index=False))

    logger.info("=" * 60)
    logger.info("Ablation study complete. Results in: %s", results_dir)
    logger.info("Figure saved to: %s", fig_dir / "fig8_leakage_ablation.png")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
