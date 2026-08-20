#!/usr/bin/env python3
"""
phase1_rerun_clean_auc.py
─────────────────────────
Re-runs the CANONICAL clean-evaluation experiment that backs the manuscript's
headline AUC table, and writes one authoritative output file.

Why this exists
───────────────
AUDIT_2026-07-20.md found the manuscript AUC table could not be reproduced.
Follow-up traced it to `outputs/results/ablation_split_variance_summary.csv`,
which turned out to be the OLDEST of the eight ablation output files — a stale
orphan from a superseded run that does not agree with its own `_raw.csv`
counterpart. See fixes/phase1_provenance.md.

Protocol (identical to src.ablation.run_split_variance_ablation)
────────────────────────────────────────────────────────────────
  * 30 repeated stratified train/test splits, seeds 42..71
  * test_size = 0.20, stratified on the label
  * top-500 gene selection by variance computed on the TRAIN FOLD ONLY,
    strictly after the split
  * StandardScaler fit on train only, applied to test
  * models + hyperparameters exactly as config/config.yaml

Deterministic: every model carries random_state=seed, so a given
(code, data, sklearn version) triple reproduces exactly.

Usage
─────
    python fixes/phase1_rerun_clean_auc.py --data-dir "D:/ALIENWARE/.../ov_tcga_pan_can_atlas_2018"

Optional:
    --thresholds 12 18 24     restrict thresholds (default: all from config)
    --n-repeats 30            number of random splits (default: 30)
    --checkpoint-dir DIR      per-threshold resume files (default: fixes/.phase1_ckpt)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 1 canonical clean-AUC re-run")
    p.add_argument("--config", default=str(ROOT / "config/config.yaml"))
    p.add_argument("--data-dir", default=None,
                   help="Override config data_dir (config's path may be stale)")
    p.add_argument("--n-repeats", type=int, default=30)
    p.add_argument("--thresholds", nargs="+", type=int, default=None)
    p.add_argument("--checkpoint-dir", default=str(ROOT / "fixes/.phase1_ckpt"))
    p.add_argument("--out", default=str(ROOT / "outputs/results/clean_auc_table.csv"))
    return p.parse_args()


def main() -> None:
    args = parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    if args.data_dir:
        cfg["data"]["data_dir"] = args.data_dir
    if args.thresholds:
        cfg["clinical"]["thresholds"] = args.thresholds

    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    from src.data_loader import load_clinical, load_expression, load_treatment
    from src.models import get_all_models, train_model
    from src.preprocessing import (
        align_expression_to_labels,
        build_labelled_survival,
        clean_expression,
        extract_survival,
        identify_platinum_patients,
    )

    ckpt_dir = Path(args.checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    print("Loading data from:", cfg["data"]["data_dir"], flush=True)
    clinical = load_clinical(cfg["data"]["data_dir"], cfg["data"]["clinical_file"])
    treatment = load_treatment(cfg["data"]["data_dir"], cfg["data"]["treatment_file"])
    expr_raw = load_expression(cfg["data"]["data_dir"], cfg["data"]["expression_file"])

    surv = extract_survival(clinical, cfg["clinical"]["time_col"], cfg["clinical"]["status_col"])
    platinum_ids = identify_platinum_patients(treatment, cfg["clinical"]["platinum_drugs"])
    labelled_dict = build_labelled_survival(
        surv, platinum_ids, cfg["clinical"]["time_col"], cfg["clinical"]["thresholds"]
    )
    expr = clean_expression(expr_raw)

    top_n = cfg["features"]["top_n_genes"]
    test_size = cfg["model"]["test_size"]
    base_seed = cfg["project"]["seed"]

    # ── per-threshold loop, checkpointed so it can resume ────────────────
    for thr, labelled in labelled_dict.items():
        ck = ckpt_dir / f"thr_{thr}.json"
        if ck.exists():
            print(f"[{thr}m] checkpoint present — skipping", flush=True)
            continue

        X, y = align_expression_to_labels(expr, labelled)
        print(f"[{thr}m] n={len(y)}  positives={int(sum(y))}  genes={X.shape[1]}", flush=True)

        rows = []
        for rep in range(args.n_repeats):
            seed = base_seed + rep
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=seed, stratify=y
            )

            # variance computed on TRAIN ONLY, after the split
            genes = X_train.var(axis=0).nlargest(top_n).index
            Xtr, Xte = X_train[genes], X_test[genes]

            # scaler fit on TRAIN ONLY
            scaler = StandardScaler()
            Xtr_sc = scaler.fit_transform(Xtr)
            Xte_sc = scaler.transform(Xte)

            for name, model in get_all_models(cfg).items():
                fitted = train_model(model, Xtr_sc, y_train)
                y_prob = fitted.predict_proba(Xte_sc)[:, 1]
                rows.append({
                    "threshold_m": thr,
                    "model": name,
                    "auc": roc_auc_score(y_test, y_prob),
                    "seed": seed,
                })
        ck.write_text(json.dumps(rows))
        print(f"[{thr}m] done — {len(rows)} rows", flush=True)

    # ── assemble ─────────────────────────────────────────────────────────
    all_rows = []
    for thr in labelled_dict:
        ck = ckpt_dir / f"thr_{thr}.json"
        if not ck.exists():
            print(f"MISSING checkpoint for {thr}m — rerun to complete", flush=True)
            sys.exit(2)
        all_rows.extend(json.loads(ck.read_text()))

    raw = pd.DataFrame(all_rows)
    raw_out = Path(args.out).with_name("clean_auc_table_raw.csv")
    raw.to_csv(raw_out, index=False)

    summary = (
        raw.groupby(["threshold_m", "model"])["auc"]
        .agg(["mean", "std", "min", "max", "count"])
        .round(4)
        .reset_index()
        .rename(columns={"count": "n_splits"})
    )
    summary.to_csv(args.out, index=False)

    print("\n=== CANONICAL CLEAN AUC TABLE ===", flush=True)
    print(summary.to_string(index=False), flush=True)
    print(f"\nwrote {args.out}", flush=True)
    print(f"wrote {raw_out}", flush=True)


if __name__ == "__main__":
    main()
