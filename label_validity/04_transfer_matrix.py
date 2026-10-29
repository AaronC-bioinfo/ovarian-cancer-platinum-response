"""
label_validity/04_transfer_matrix.py
────────────────────────────────────
Q2 analysis A4 — label-transfer matrix
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A4).

Question: does a classifier trained on TCGA-OV with a platinum-response label
transfer to GSE63885 better than one trained on an OS-threshold label?

DESIGN — validation/06_external_validation_v2.py with ONLY the training label
swapped. Everything else is copied unchanged: common-gene restriction, top 500
variance genes selected in the TCGA training set per label, variant P (primary:
log2(RSEM+1), TCGA scaler fit on training data, GEO z-scored within GEO) and
variant S (sensitivity: raw RSEM as in the paper), LR/RF/SVM from
config/config.yaml (seed 42), GEO test labels `clinical` (SD/PD vs CR/PR) and
`dfs` (platinum-resistant DFS < 180 d vs sensitive), AUC with 2,000-resample
stratified bootstrap CI (seed 42). GSE63885 is never used for fitting or selection.

Training labels (from label_validity/outputs/labels_master.csv, A1):
  label_platinum (primary), label_pfiplat6, label_response, label_os18, label_os24;
  label_os12 kept only for the reproduction check (supplement).
  Each label is turned into the {PATIENT_ID, response} frame that
  src.preprocessing.align_expression_to_labels expects, so patient alignment and
  ordering are identical to 06.

Run on the host (sklearn 1.9.0):
  C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe label_validity\\04_transfer_matrix.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"

Outputs → label_validity/outputs/a4_transfer_results.csv, 04_transfer_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already known (disclosed): v2 OS-trained results
(validation/outputs/external_validation_v2_results.csv), variant P, dfs label:
12m 0.498–0.536, 18m 0.545–0.581, 24m 0.610–0.674; clinical label 0.480–0.575;
1 of 36 CIs excluded 0.5. A1 training n: platinum 145 (41 resistant),
pfiplat6 188 (53), response 219 (35), OS18 206 (22), OS24 199 (36).

  C1  REPRODUCTION CHECK: rows for label_os12/os18/os24 equal the v2 results
      file (all 36 AUCs and CIs to 4 dp). If not, the harness changed and the
      remaining rows are not interpretable until explained.
  P1  Variant P, dfs label: mean AUC over the 3 models for label_platinum is
      higher than for label_os18 and higher than for label_os24.
  P2  All variant-P AUCs (5 main labels × 3 models × 2 GEO labels = 30) < 0.70.
  P3  At most 3 of those 30 variant-P CIs exclude 0.5.
  P4  GEO clinical label (10 non-responders): every variant-P CI includes 0.5.
  P5  Variant S mean AUC ≤ variant P mean AUC for the platinum-trained models.

DECISION RULE (pre-specified):
  "Label choice improves transfer" if, in variant P on the dfs label,
  label_platinum or label_pfiplat6 has ≥ 2 of 3 models with CI excluding 0.5
  AND its mean AUC exceeds both OS labels' means.
  Otherwise: "transfer remains weak whatever the training label"; A5 then
  separates label mismatch from platform mismatch within TCGA.
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
from src.data_loader import load_expression
from src.models import get_all_models
from src.preprocessing import align_expression_to_labels, clean_expression

EXT = ROOT / "data" / "external"
OUT = ROOT / "label_validity" / "outputs"
V2 = ROOT / "validation" / "outputs" / "external_validation_v2_results.csv"
TRAIN_LABELS = ["label_platinum", "label_pfiplat6", "label_response", "label_os18", "label_os24", "label_os12"]
OS_THR = {"label_os12": 12, "label_os18": 18, "label_os24": 24}


# ── copied unchanged from validation/06_external_validation_v2.py ──────────
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
# ───────────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--config", default=str(ROOT / "config" / "config.yaml"))
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    expr = clean_expression(load_expression(a.data_dir, cfg["data"]["expression_file"]))

    master = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    geo = pd.read_csv(EXT / "GSE63885_expr_gene.csv", index_col=0)
    meta = pd.read_csv(EXT / "harmonised_metadata.csv").set_index("sample_id")
    meta = meta.loc[[s for s in geo.columns if s in meta.index]]
    labels = {"clinical": pd.to_numeric(meta["platinum_label_clinical"], errors="coerce"),
              "dfs": pd.to_numeric(meta["platinum_label_dfs.y"], errors="coerce")}
    expr = expr[~expr.index.duplicated()]
    geo = geo[~geo.index.duplicated()]
    common = sorted(set(expr.index) & set(geo.index))
    print(f"sklearn {sklearn.__version__} | common genes {len(common)} | GEO samples {geo.shape[1]}")

    rows = []
    for tl in TRAIN_LABELS:
        lab = master[tl].dropna().astype(int).rename("response").rename_axis("PATIENT_ID").reset_index()
        X_raw, y = align_expression_to_labels(expr.loc[common], lab)
        print(f"[{tl}] TCGA n={len(y)} non-responders={int(y.sum())}")
        for variant in ("P", "S"):
            Xsel = np.log2(X_raw + 1) if variant == "P" else X_raw
            genes = Xsel.var(axis=0).nlargest(cfg["features"]["top_n_genes"]).index
            sc = StandardScaler().fit(Xsel[genes])
            Xtr = sc.transform(Xsel[genes])
            G = zscore_within(geo.loc[genes].T)[genes].values
            for name, model in get_all_models(cfg).items():
                model.fit(Xtr, y.values)
                prob = model.predict_proba(G)[:, 1]
                for ln, yl in labels.items():
                    m = yl.notna().values
                    yy = yl[m].astype(int).values; pp = prob[m]
                    auc = roc_auc_score(yy, pp); lo, hi = boot_ci(yy, pp)
                    rows.append(dict(train_label=tl, variant=variant, model=name, label=ln,
                                     train_n=len(y), train_nonresponder=int(y.sum()),
                                     n=int(m.sum()), n_nonresponder=int(yy.sum()),
                                     auc=round(auc, 4), ci_lo=round(lo, 4), ci_hi=round(hi, 4),
                                     ci_excludes_half=bool(lo > 0.5 or hi < 0.5),
                                     supplement=tl == "label_os12"))
                    print(f"   {variant} {name:20s} {ln:8s} AUC {auc:.3f} [{lo:.3f}, {hi:.3f}]")
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "a4_transfer_results.csv", index=False)

    # ── C1 reproduction check against the v2 file ──────────────────────────
    v2 = pd.read_csv(V2)
    osr = df[df.train_label.isin(OS_THR)].copy()
    osr["threshold_m"] = osr.train_label.map(OS_THR)
    j = osr.merge(v2, on=["variant", "threshold_m", "model", "label"], suffixes=("", "_v2"))
    diff = (j[["auc", "ci_lo", "ci_hi"]].values - j[["auc_v2", "ci_lo_v2", "ci_hi_v2"]].values)
    c1 = len(j) == 36 and np.abs(diff).max() < 1e-4
    c1_txt = (f"C1 reproduction: {len(j)}/36 rows matched; max |Δ| = {np.abs(diff).max():.5f} → "
              + ("**PASS**" if c1 else "**FAIL — stop and explain before interpreting**"))

    P = df[(df.variant == "P") & ~df.supplement]
    mean_dfs = P[P.label == "dfs"].groupby("train_label").auc.mean()
    n_excl_dfs = P[P.label == "dfs"].groupby("train_label").ci_excludes_half.sum()
    S = df[(df.variant == "S") & ~df.supplement]
    better = lambda l: mean_dfs[l] > mean_dfs["label_os18"] and mean_dfs[l] > mean_dfs["label_os24"]
    dec = ("Label choice improves transfer"
           if any(n_excl_dfs[l] >= 2 and better(l) for l in ("label_platinum", "label_pfiplat6"))
           else "Transfer remains weak whatever the training label")

    order = ["label_platinum", "label_pfiplat6", "label_response", "label_os18", "label_os24"]
    mat = P.pivot_table(index=["train_label", "model"], columns="label", values="auc").reindex(order, level=0)
    L = ["# A4 — label-transfer matrix (TCGA-OV → GSE63885)", "",
         f"sklearn {sklearn.__version__}; common genes {len(common)}. Harness = validation/06_external_validation_v2.py, training label swapped.", "",
         c1_txt, "",
         "## Variant P (primary): AUC by training label × model × GEO label", "",
         "```", mat.round(3).to_string(), "```", "",
         "Full table with 95% CIs: a4_transfer_results.csv.", "",
         "## Predictions vs observed", "",
         "- P1 mean dfs AUC (variant P) by training label: " + ", ".join(f"{l} {mean_dfs[l]:.3f}" for l in order)
         + f" → platinum > OS18 and > OS24: {better('label_platinum')}",
         f"- P2 max variant-P AUC: {P.auc.max():.3f} (predicted all < 0.70)",
         f"- P3 variant-P CIs excluding 0.5: {int(P.ci_excludes_half.sum())} of {len(P)} (predicted ≤ 3); "
         + "; ".join(f"{r.train_label}/{r.model}/{r.label} {r.auc:.3f} [{r.ci_lo:.3f}, {r.ci_hi:.3f}]"
                     for r in P[P.ci_excludes_half].itertuples()),
         f"- P4 clinical label CIs excluding 0.5: {int(P[P.label == 'clinical'].ci_excludes_half.sum())} (predicted 0)",
         f"- P5 platinum-trained mean AUC: variant S {S[S.train_label == 'label_platinum'].auc.mean():.3f} vs "
         f"variant P {P[P.train_label == 'label_platinum'].auc.mean():.3f} (predicted S ≤ P)",
         "", f"**Decision rule: {dec}.** dfs CIs excluding 0.5 per label: "
         + ", ".join(f"{l} {int(n_excl_dfs[l])}/3" for l in order)]
    (OUT / "04_transfer_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
