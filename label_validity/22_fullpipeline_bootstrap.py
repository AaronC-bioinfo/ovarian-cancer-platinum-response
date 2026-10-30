#!/usr/bin/env python3
"""
label_validity/22_fullpipeline_bootstrap.py
───────────────────────────────────────────
A22 — full-pipeline uncertainty for the controlled comparison of training labels (A16). Post hoc.
Writing started 2026-10-30 00:31 ET, BEFORE this script was run (run times are recorded in the outputs), in
response to a fourth review (point 11: resampling fixed, averaged out-of-fold scores does not repeat feature
selection, model fitting, training-sample variation or fold allocation). Known before writing: the A16 results
(ΔAUC_24 −0.005, conditional interval −0.105 to +0.087; ΔAUC_18 +0.080 [−0.045, +0.201]; reverse on OS24 −0.069
[−0.236, +0.081]). Not seen: any result of this analysis.

Design (same patients, data and pipeline as A16, 16_controlled_label_comparison.py): 134 patients; log2(RSEM + 1);
genes shared with GSE63885; per fit, 500 highest-variance genes and StandardScaler computed on the training sample;
LR, RF, SVM from config/config.yaml. Out-of-bag bootstrap: in each of B = 500 replicates (numpy default_rng(1000 + b)),
patients are drawn with replacement within the platinum-resistant and platinum-sensitive groups (stratified); the
whole pipeline is fitted on the drawn sample for each training label (platinum, OS18, OS24) and each model, and the
patients not drawn (out of bag) are scored. Per replicate, for each contrast as in A16 (primary ΔAUC_24: platinum-
trained − OS24-trained, target platinum status; ΔAUC_18; reverse on the OS24 target), the AUC difference is computed
per model on the out-of-bag patients and averaged over the three models; a replicate contributes to a contrast only
if its out-of-bag target has both classes, and is skipped if any training label has one class in the drawn sample.
Reported: number of usable replicates; median and 2.5th/97.5th percentiles of the replicate differences (the
full-pipeline interval); the A16 conditional estimate and interval alongside. Out-of-bag AUCs are pessimistic
(fits use about 63% of distinct patients); the interval describes variability of the whole procedure, centred on
the out-of-bag differences.

PREDICTION
  P1  The full-pipeline 95% interval for ΔAUC_24 is wider than the conditional interval (width 0.192).
DECISION RULE (for the manuscript)
  * The full-pipeline interval becomes the main uncertainty reported for the controlled comparison (abstract and
    Results), with the conditional interval as secondary. If the full-pipeline interval for ΔAUC_24 excludes 0,
    the text says so; otherwise it states that no clear difference was demonstrated.

Run in chunks (from the repo root): python label_validity/22_fullpipeline_bootstrap.py --data-dir "<...>/ov_tcga_pan_can_atlas_2018" --start 0 --stop 100
  (repeat for 100–200, …, 400–500), then: python label_validity/22_fullpipeline_bootstrap.py --combine
Correction before any result: the first attempt (00:31 ET) stopped at replicate 0 with "Input X contains NaN", because numpy
var() returns NaN for genes with missing values and those sorted first; gene ranking now uses nanvar (as pandas .var()
in A16). No output was produced by the failed attempt.
Outputs → label_validity/outputs/a22_chunks/a22_boot_<start>_<stop>.csv, a22_fullpipeline_replicates.csv,
          a22_ENVIRONMENT.txt, 22_fullpipeline_bootstrap_summary.md
"""
from __future__ import annotations

import argparse
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "label_validity" / "outputs"
CH = OUT / "a22_chunks"
TRAIN = ["label_platinum", "label_os18", "label_os24"]
TOPN, B = 500, 500
CONTRASTS = [("primary_dAUC24", "label_platinum", "label_platinum", "label_os24"),
             ("dAUC18", "label_platinum", "label_platinum", "label_os18"),
             ("reverse_OS24_target", "label_os24", "label_os24", "label_platinum")]


def run_chunk(data_dir: str, start: int, stop: int) -> None:
    import sklearn
    import yaml
    from sklearn.base import clone
    from sklearn.metrics import roc_auc_score
    from sklearn.preprocessing import StandardScaler
    sys.path.insert(0, str(ROOT))
    from src.data_loader import load_expression
    from src.models import get_all_models
    from src.preprocessing import clean_expression
    t0 = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    cfg = yaml.safe_load(open(ROOT / "config" / "config.yaml"))
    expr = clean_expression(load_expression(data_dir, cfg["data"]["expression_file"]))
    expr = expr[~expr.index.duplicated()]
    geo = pd.read_csv(ROOT / "data" / "external" / "GSE63885_expr_gene.csv", index_col=0, usecols=[0])
    common = sorted(set(expr.index) & set(geo.index[~geo.index.duplicated()]))
    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    m = m[m["in_rnaseq"].astype(bool)].dropna(subset=TRAIN)
    ids = sorted(set(m.index) & set(expr.columns)); m = m.loc[ids]
    assert len(ids) == 134
    X = np.log2(expr.loc[common, ids].T + 1).values
    y = {l: m[l].astype(int).values for l in TRAIN}
    models = get_all_models(cfg)
    res_i = np.where(y["label_platinum"] == 1)[0]; sen_i = np.where(y["label_platinum"] == 0)[0]
    rows = []
    for b in range(start, stop):
        rng = np.random.default_rng(1000 + b)
        draw = np.concatenate([rng.choice(res_i, len(res_i), replace=True), rng.choice(sen_i, len(sen_i), replace=True)])
        oob = np.setdiff1d(np.arange(len(ids)), draw)
        if any(len(np.unique(y[l][draw])) < 2 for l in TRAIN):
            rows.append(dict(replicate=b, skipped="single-class training label")); continue
        Xtr = X[draw]
        v = np.nanvar(Xtr, axis=0, ddof=1); v[np.isnan(v)] = -np.inf   # as pandas .var() in A16 (NaN skipped)
        g = np.argsort(v)[::-1][:TOPN]
        sc = StandardScaler().fit(Xtr[:, g]); A, Bm = sc.transform(Xtr[:, g]), sc.transform(X[oob][:, g])
        score = {}
        for tl in TRAIN:
            for mn, base in models.items():
                score[(tl, mn)] = clone(base).fit(A, y[tl][draw]).predict_proba(Bm)[:, 1]
        r = dict(replicate=b, skipped="", n_oob=len(oob))
        for name, target, a_lab, b_lab in CONTRASTS:
            yt = y[target][oob]
            r[f"{name}_oob_pos"] = int(yt.sum())
            if len(np.unique(yt)) < 2:
                r[name] = np.nan; continue
            r[name] = float(np.mean([roc_auc_score(yt, score[(a_lab, mn)]) - roc_auc_score(yt, score[(b_lab, mn)]) for mn in models]))
        rows.append(r)
    CH.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows); df["chunk_started"] = t0; df["chunk_finished"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    df.to_csv(CH / f"a22_boot_{start:03d}_{stop:03d}.csv", index=False)
    (OUT / "a22_ENVIRONMENT.txt").write_text(f"Python {platform.python_version()}; scikit-learn {sklearn.__version__}; numpy {np.__version__}; pandas {pd.__version__}\n", encoding="utf-8")
    print(f"chunk {start}-{stop} done: {len(df)} replicates, {int((df.skipped != '').sum())} skipped")


def combine() -> None:
    files = sorted(CH.glob("a22_boot_*.csv"))
    df = pd.concat([pd.read_csv(f) for f in files]).sort_values("replicate")
    assert sorted(df.replicate) == list(range(B)), "missing replicates"
    df.to_csv(OUT / "a22_fullpipeline_replicates.csv", index=False)
    a16 = pd.read_csv(OUT / "a16_paired_differences.csv").set_index("contrast")
    rows = []
    for name, *_ in CONTRASTS:
        v = df[name].dropna()
        lo, med, hi = np.percentile(v, [2.5, 50, 97.5])
        c = a16.loc[name]
        rows.append(dict(contrast=name, usable_replicates=len(v), oob_median=med, full_lo=lo, full_hi=hi, full_width=hi - lo,
                         conditional_estimate=c.delta_repeat_averaged_scores, conditional_lo=c.boot_lo, conditional_hi=c.boot_hi,
                         conditional_width=c.boot_hi - c.boot_lo, full_excludes_0=bool(lo > 0 or hi < 0)))
    s = pd.DataFrame(rows)
    p = s.set_index("contrast").loc["primary_dAUC24"]
    env = (OUT / "a22_ENVIRONMENT.txt").read_text(encoding="utf-8").strip()
    L = ["# A22 — Full-pipeline (out-of-bag bootstrap) uncertainty for the controlled label comparison", "", env, "",
         f"Chunks run: {df.chunk_started.min()} – {df.chunk_finished.max()}; skipped replicates: {int(df.skipped.fillna('').ne('').sum())}", "",
         "```", s.round(3).to_string(index=False), "```", "",
         f"P1 (full-pipeline interval for ΔAUC_24 wider than the conditional interval): {'held' if p.full_width > p.conditional_width else 'FAILED'} "
         f"({p.full_width:.3f} vs {p.conditional_width:.3f}).",
         f"Decision rule: full-pipeline interval for ΔAUC_24 excludes 0: {bool(p.full_excludes_0)}.", ""]
    (OUT / "22_fullpipeline_bootstrap_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir"); ap.add_argument("--start", type=int); ap.add_argument("--stop", type=int)
    ap.add_argument("--combine", action="store_true")
    a = ap.parse_args()
    combine() if a.combine else run_chunk(a.data_dir, a.start, a.stop)
