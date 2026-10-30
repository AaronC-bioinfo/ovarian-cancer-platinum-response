#!/usr/bin/env python3
"""
label_validity/16_controlled_label_comparison.py
────────────────────────────────────────────────
A16 — controlled comparison of training labels for expression classifiers: same patients, same outer
folds, paired AUC differences with patient-bootstrap confidence intervals.

Written 2026-10-29 ~22:10 ET, BEFORE the run, in response to an external review of manuscript v5
(point 4: "the classifier experiment does not cleanly isolate the effect of label choice … report paired
uncertainty for the AUC differences"). A5 compared labels on different patient sets and class balances;
its pre-specified rule found a label effect of +0.060 that reached 0.05 in only 3 of 5 repeats.

DISCLOSURE — seen before writing: all A5 results (a5_cross_label_repeats.csv). Not seen: any analysis
restricted to a common patient set, any paired difference, any bootstrap interval for a difference.

Population: platinum-treated patients with RNA-seq data (labels_master in_rnaseq) in whom label_platinum,
label_os18 and label_os24 are ALL determinate. Every label is therefore trained and evaluated on exactly
the same patients.
Pipeline: identical to A5 (05_cross_label_cv.py): log2(RSEM + 1); the genes shared with GSE63885;
500 highest-variance genes and StandardScaler fitted on the training fold only; LR, RF, SVM from
config/config.yaml (balanced class weights, seed 42).
Folds: 20 repeats of stratified 5-fold CV (stratified on label_platinum; random_state = repeat). In each
training fold, one model per training label is fitted on the same training patients; all are scored on the
same held-out patients.
Quantities (all on the same patients):
  * Per repeat: pooled out-of-fold AUC for each training label × model × target label.
  * Primary: ΔAUC_24 = AUC(platinum-trained → platinum status) − AUC(OS24-trained → platinum status),
    mean over the three models. Secondary: ΔAUC_18 (OS18-trained), and the reverse on the OS24 target:
    AUC(OS24-trained → OS24) − AUC(platinum-trained → OS24).
  * Uncertainty: for each model, out-of-fold scores are averaged over the 20 repeats (one score per patient);
    the mean-over-models ΔAUC is recomputed in 2,000 bootstrap resamples of patients stratified by the target
    label (numpy default_rng(42)); 95% percentile interval. The spread of ΔAUC across repeats is reported
    separately and is NOT a confidence interval.

PREDICTIONS
  Q1  Mean ΔAUC_24 (platinum-trained minus OS24-trained, on platinum status) lies between 0 and +0.10.
  Q2  The 95% bootstrap interval for ΔAUC_24 includes 0.
  Q3  ΔAUC_18 > 0, with a 95% interval that includes 0.
  Q4  Reverse on the OS24 target: AUC(OS24-trained) − AUC(platinum-trained) > 0, with a 95% interval
      that includes 0.

DECISION RULES (for the manuscript)
  * If the ΔAUC_24 interval excludes 0 (positive), the manuscript states that, in the same patients,
    platinum-trained models predicted platinum status better than OS-trained models, with the estimate and
    interval.
  * If it includes 0, the manuscript states that a difference larger than the interval's upper bound is
    unlikely but that no difference was detected, and it withdraws any claim that label choice changes
    classifier performance; A5 is then reported as descriptive only.

Run (Windows host, pinned environment; from the repo root):
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\16_controlled_label_comparison.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Outputs → label_validity/outputs/a16_repeats.csv, a16_oof_scores.csv, a16_paired_differences.csv,
          a16_ENVIRONMENT.txt, 16_controlled_label_comparison_summary.md
"""
from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
import yaml
from sklearn.base import clone
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.data_loader import load_expression  # noqa: E402
from src.models import get_all_models  # noqa: E402
from src.preprocessing import clean_expression  # noqa: E402

EXT = ROOT / "data" / "external"
OUT = ROOT / "label_validity" / "outputs"
TRAIN = ["label_platinum", "label_os18", "label_os24"]
REPEATS, FOLDS, TOPN, NBOOT = 20, 5, 500, 2000


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    out = Path(a.out)
    cfg = yaml.safe_load(open(ROOT / "config" / "config.yaml"))
    expr = clean_expression(load_expression(a.data_dir, cfg["data"]["expression_file"]))
    expr = expr[~expr.index.duplicated()]
    geo = pd.read_csv(EXT / "GSE63885_expr_gene.csv", index_col=0, usecols=[0])
    common = sorted(set(expr.index) & set(geo.index[~geo.index.duplicated()]))

    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    m = m[m["in_rnaseq"].astype(bool)].dropna(subset=TRAIN)
    ids = sorted(set(m.index) & set(expr.columns))
    m = m.loc[ids]
    X = np.log2(expr.loc[common, ids].T + 1)
    y = {l: m[l].astype(int) for l in TRAIN}
    models = get_all_models(cfg)
    env = (f"Python {platform.python_version()}; scikit-learn {sklearn.__version__}; numpy {np.__version__}; "
           f"pandas {pd.__version__}")
    (out / "a16_ENVIRONMENT.txt").write_text(env + "\n", encoding="utf-8")
    print(env, f"| patients {len(ids)} | genes {len(common)} | platinum-resistant {int(y['label_platinum'].sum())} "
               f"| OS18 {int(y['label_os18'].sum())} | OS24 {int(y['label_os24'].sum())}")

    rows, oof_all = [], []
    for rep in range(REPEATS):
        oof = {(tl, mn): pd.Series(np.nan, index=ids) for tl in TRAIN for mn in models}
        skf = StratifiedKFold(n_splits=FOLDS, shuffle=True, random_state=rep)
        for tr_idx, te_idx in skf.split(ids, y["label_platinum"].values):
            tr_ids, te_ids = [ids[i] for i in tr_idx], [ids[i] for i in te_idx]
            Xtr = X.loc[tr_ids]
            genes = Xtr.var(axis=0).nlargest(TOPN).index
            sc = StandardScaler().fit(Xtr[genes])
            A, B = sc.transform(Xtr[genes]), sc.transform(X.loc[te_ids, genes])
            for tl in TRAIN:
                for mn, base in models.items():
                    mdl = clone(base).fit(A, y[tl].loc[tr_ids].values)
                    oof[(tl, mn)].loc[te_ids] = mdl.predict_proba(B)[:, 1]
        for (tl, mn), s in oof.items():
            oof_all.append(pd.DataFrame({"repeat": rep, "train_label": tl, "model": mn, "patient": s.index, "score": s.values}))
            for te in ["label_platinum", "label_os24", "label_os18"]:
                rows.append(dict(repeat=rep, train_label=tl, test_label=te, model=mn, n=len(ids),
                                 n_pos=int(y[te].sum()), auc=roc_auc_score(y[te].values, s.loc[ids].values)))
        print(f"repeat {rep} done", flush=True)
    r = pd.DataFrame(rows); r.to_csv(out / "a16_repeats.csv", index=False)
    oo = pd.concat(oof_all); oo.to_csv(out / "a16_oof_scores.csv", index=False)

    # per-patient scores averaged over repeats
    avg = oo.groupby(["train_label", "model", "patient"]).score.mean().unstack("patient")
    mnames = list(models)

    def delta(target, a_lab, b_lab, idx):
        yt = y[target].values[idx]
        d = []
        for mn in mnames:
            sa = avg.loc[(a_lab, mn)].reindex(ids).values[idx]
            sb = avg.loc[(b_lab, mn)].reindex(ids).values[idx]
            d.append(roc_auc_score(yt, sa) - roc_auc_score(yt, sb))
        return float(np.mean(d))

    contrasts = [("primary_dAUC24", "label_platinum", "label_platinum", "label_os24"),
                 ("dAUC18", "label_platinum", "label_platinum", "label_os18"),
                 ("reverse_OS24_target", "label_os24", "label_os24", "label_platinum")]
    rng = np.random.default_rng(42)
    allidx = np.arange(len(ids))
    res = []
    for name, target, a_lab, b_lab in contrasts:
        est = delta(target, a_lab, b_lab, allidx)
        yt = y[target].values
        pos, neg = np.where(yt == 1)[0], np.where(yt == 0)[0]
        bs = np.empty(NBOOT)
        for i in range(NBOOT):
            idx = np.concatenate([rng.choice(pos, len(pos)), rng.choice(neg, len(neg))])
            bs[i] = delta(target, a_lab, b_lab, idx)
        lo, hi = np.percentile(bs, [2.5, 97.5])
        per_rep = (r[(r.test_label == target) & (r.train_label == a_lab)].groupby("repeat").auc.mean()
                   - r[(r.test_label == target) & (r.train_label == b_lab)].groupby("repeat").auc.mean())
        res.append(dict(contrast=name, target=target, label_a=a_lab, label_b=b_lab, n=len(ids), n_pos=int(yt.sum()),
                        delta_repeat_averaged_scores=est, boot_lo=float(lo), boot_hi=float(hi),
                        ci_includes_0=bool(lo <= 0 <= hi), per_repeat_mean=float(per_rep.mean()),
                        per_repeat_min=float(per_rep.min()), per_repeat_max=float(per_rep.max()),
                        repeats_ge_0_05=int((per_rep >= 0.05).sum())))
    pdiff = pd.DataFrame(res); pdiff.to_csv(out / "a16_paired_differences.csv", index=False)

    mean_auc = r.groupby(["train_label", "test_label"]).auc.agg(["mean", "min", "max"]).round(3)
    L = ["# A16 — Controlled comparison of training labels (same patients, same folds)", "", env,
         f"Patients: {len(ids)} (platinum-resistant {int(y['label_platinum'].sum())}; OS18 {int(y['label_os18'].sum())}; "
         f"OS24 {int(y['label_os24'].sum())}). {REPEATS} × {FOLDS}-fold CV; {NBOOT} stratified patient bootstraps.", "",
         "## Mean AUC over 3 models and 20 repeats (min–max across model × repeat)", "", "```", mean_auc.to_string(), "```", "",
         "## Paired differences (mean over models; scores averaged over repeats)", ""]
    for p in pdiff.itertuples():
        L.append(f"- {p.contrast} ({p.label_a} − {p.label_b} on {p.target}): {p.delta_repeat_averaged_scores:+.3f} "
                 f"[{p.boot_lo:+.3f}, {p.boot_hi:+.3f}]; CI includes 0: {p.ci_includes_0}; per-repeat mean "
                 f"{p.per_repeat_mean:+.3f} (range {p.per_repeat_min:+.3f} to {p.per_repeat_max:+.3f}; ≥ 0.05 in {p.repeats_ge_0_05}/20)")
    L += ["", "## Prediction scorecard", "", "(to be completed after the run)", ""]
    (out / "16_controlled_label_comparison_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
