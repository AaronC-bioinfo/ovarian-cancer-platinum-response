"""
Corrected external validation on GSE63885. Written 2026-10-29; predictions
recorded BELOW, BEFORE the first run (DEC-019).

WHY THIS REPLACES validate_external.py
  validate_external.py re-selected "top-500 variance genes" from
  data/external/tcga_corrected_expression.csv, in which every gene has the
  same variance (0.994737; genes were z-scored before ComBat). The selection
  was therefore arbitrary and did not match the genes the saved models were
  trained on, so the models were scored on the wrong features. Its AUC ~0.5
  and the post-ComBat r = -0.007 (a correlation of per-gene means that are ~0
  by construction) are not valid evidence and are withdrawn.

DESIGN (fixed before running)
  Training: TCGA-OV PanCanAtlas 2018, platinum-treated, OS-threshold labels at
    12/18/24 months, built with the paper's own src/ functions (same cohorts
    as Table 2). The whole labelled TCGA cohort is the training set; GSE63885
    is never used for any fitting or selection.
  Genes: restricted to symbols present on both platforms; top 500 by variance
    in the TCGA training cohort (per threshold). The SAME 500 genes, in the
    same order, are passed to the model for GEO.
  Variant P (primary): TCGA log2(RSEM+1); selection on log2 values; each
    gene z-scored within TCGA for training and within GEO for testing (GEO
    data are log2 RMA, gene-level, data/external/GSE63885_expr_gene.csv).
  Variant S (secondary, pipeline-faithful): selection and TCGA scaling on raw
    RSEM as in the paper; GEO genes z-scored within GEO.
  Models: LR, RF, SVM with config/config.yaml hyperparameters, seed 42.
  Test labels (GEO, 1 = non-responder, matching TCGA coding):
    clinical: SD/PD vs CR/PR after first-line chemotherapy;
    dfs: platinum-resistant (DFS < 180 days) vs sensitive.
  Metric: AUC with 95% CI from 2,000 stratified bootstrap resamples (seed 42).
  36 AUCs in total (2 variants x 3 models x 3 thresholds x 2 labels).

PREDICTIONS
  P1. Primary variant: most AUCs lie between 0.40 and 0.70. For the clinical
      label (only 10 non-responders), all 95% CIs include 0.5.
  P2. Primary, dfs label, 18m and 24m models: at least 4 of 6 AUC point
      estimates exceed 0.5, but at most 2 of the 6 CIs exclude 0.5.
  P3. 12m models: all CIs include 0.5 (12m is unstable even within TCGA).
  P4. Variant S performs no better than variant P on average.
  Decision rule: the manuscript reports variant P as the external-validation
  result and variant S as a sensitivity analysis; transfer is described as
  successful only where the 95% CI excludes 0.5. No mechanism (e.g. platform
  incompatibility) is claimed, because none is tested here.

Outputs: validation/outputs/external_validation_v2_results.csv
         validation/outputs/external_validation_v2_summary.md
Run:     python validation/06_external_validation_v2.py --data-dir <ov_tcga_pan_can_atlas_2018 dir>
"""
import argparse, sys
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
import sklearn

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.data_loader import load_clinical, load_expression, load_treatment
from src.models import get_all_models
from src.preprocessing import (align_expression_to_labels, build_labelled_survival,
                               clean_expression, extract_survival, identify_platinum_patients)

EXT = ROOT / "data" / "external"
OUT = ROOT / "validation" / "outputs"


def zscore_within(df):
    sd = df.std(axis=0, ddof=0).replace(0, np.nan)
    return ((df - df.mean(axis=0)) / sd).fillna(0.0)


def boot_ci(y, p, n=2000, seed=42):
    rng = np.random.default_rng(seed)
    y = np.asarray(y); p = np.asarray(p)
    i1, i0 = np.where(y == 1)[0], np.where(y == 0)[0]
    aucs = []
    for _ in range(n):
        b = np.concatenate([rng.choice(i1, len(i1)), rng.choice(i0, len(i0))])
        aucs.append(roc_auc_score(y[b], p[b]))
    return np.percentile(aucs, [2.5, 97.5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--config", default=str(ROOT / "config" / "config.yaml"))
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    d = a.data_dir
    clinical = load_clinical(d, cfg["data"]["clinical_file"])
    treatment = load_treatment(d, cfg["data"]["treatment_file"])
    expr = clean_expression(load_expression(d, cfg["data"]["expression_file"]))
    surv = extract_survival(clinical, cfg["clinical"]["time_col"], cfg["clinical"]["status_col"])
    plat = identify_platinum_patients(treatment, cfg["clinical"]["platinum_drugs"])
    labelled = build_labelled_survival(surv, plat, cfg["clinical"]["time_col"], cfg["clinical"]["thresholds"])

    geo = pd.read_csv(EXT / "GSE63885_expr_gene.csv", index_col=0)          # genes x samples, log2 RMA
    meta = pd.read_csv(EXT / "harmonised_metadata.csv").set_index("sample_id")
    meta = meta.loc[[s for s in geo.columns if s in meta.index]]
    labels = {"clinical": pd.to_numeric(meta["platinum_label_clinical"], errors="coerce"),
              "dfs": pd.to_numeric(meta["platinum_label_dfs.y"], errors="coerce")}
    expr = expr[~expr.index.duplicated()]
    geo = geo[~geo.index.duplicated()]
    common = sorted(set(expr.index) & set(geo.index))
    print(f"sklearn {sklearn.__version__} | common genes {len(common)} | GEO samples {geo.shape[1]}")

    rows = []
    for thr, lab in labelled.items():
        X_raw, y = align_expression_to_labels(expr.loc[common], lab)
        print(f"[{thr}m] TCGA n={len(y)} non-responders={int(y.sum())}")
        for variant in ("P", "S"):
            Xsel = np.log2(X_raw + 1) if variant == "P" else X_raw
            genes = Xsel.var(axis=0).nlargest(cfg["features"]["top_n_genes"]).index
            sc = StandardScaler().fit(Xsel[genes])
            Xtr = sc.transform(Xsel[genes])
            G = zscore_within(geo.loc[genes].T)[genes].values       # same genes, same order
            for name, model in get_all_models(cfg).items():
                model.fit(Xtr, y.values)
                prob = model.predict_proba(G)[:, 1]
                for ln, yl in labels.items():
                    m = yl.notna().values
                    yy = yl[m].astype(int).values; pp = prob[m]
                    auc = roc_auc_score(yy, pp); lo, hi = boot_ci(yy, pp)
                    rows.append(dict(variant=variant, threshold_m=thr, model=name, label=ln,
                                     n=int(m.sum()), n_nonresponder=int(yy.sum()),
                                     auc=round(auc, 4), ci_lo=round(lo, 4), ci_hi=round(hi, 4),
                                     ci_excludes_half=bool(lo > 0.5 or hi < 0.5)))
                    print(f"   {variant} {name:20s} {ln:8s} AUC {auc:.3f} [{lo:.3f}, {hi:.3f}]")
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "external_validation_v2_results.csv", index=False)
    md = ["# Corrected external validation (GSE63885)", "",
          f"sklearn {sklearn.__version__}; common genes {len(common)}; predictions in script header.", "",
          df.to_markdown(index=False), ""]
    (OUT / "external_validation_v2_summary.md").write_text("\n".join(md), encoding="utf-8")
    print("wrote", OUT / "external_validation_v2_results.csv")


if __name__ == "__main__":
    main()
