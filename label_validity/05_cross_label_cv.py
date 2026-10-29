"""
label_validity/05_cross_label_cv.py
───────────────────────────────────
Q2 analysis A5 — within-TCGA cross-label prediction
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A5).

Question: inside TCGA-OV alone, do models trained on one label predict another
label in held-out patients? This separates "label mismatch" from "platform /
cohort mismatch" as the cause of the weak transfer seen in A4.

DESIGN (fixed before running)
  Patients: platinum-treated with RNA-seq (labels_master.csv, in_rnaseq; n = 251).
  Labels: label_platinum (primary), label_pfiplat6 (sensitivity), label_os18,
    label_os24. 4 training labels × 4 test labels; the diagonal is each label's
    own cross-validated ceiling.
  Folds: StratifiedKFold(5, shuffle) on all 251 patients, stratified on
    label_platinum with undetermined as its own stratum; 5 repeats (seeds 0–4).
  Per fold and training label: train on fold-train patients whose training
    label is determinate. Inside that training set only: log2(RSEM + 1), top 500
    genes by variance (genes restricted to the 15,994 symbols common with
    GSE63885, exactly as A4), StandardScaler fit; transform the test fold.
    Models LR / RF / SVM from config/config.yaml (seed 42). Hyperparameters are
    fixed, so there is no inner tuning loop — selection and scaling inside each
    training fold is the whole of the nesting.
  Each fitted model scores every test-fold patient; per repeat, out-of-fold
  scores are pooled and one AUC is computed for each test label on the patients
  where that label is determinate. Reported: mean AUC over the 5 repeats with
  min–max.
  Same preprocessing as A4's primary variant (P), so A5's diagonal is
  comparable with A4's GEO AUCs.

Run on the host (sklearn 1.9.0), from the project root:
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\05_cross_label_cv.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Outputs → label_validity/outputs/a5_cross_label_repeats.csv, 05_cross_label_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already known (disclosed): v2 clean within-TCGA AUC (raw RSEM, single split,
30 repeats): 18m 0.62–0.67, 24m 0.68–0.73 by model. A4 GEO dfs AUC, mean of 3
models: platinum-trained 0.589, OS24-trained 0.626. A2: κ(OS18, platinum) 0.14,
κ(OS24, platinum) 0.25, κ(platinum, pfiplat6) 0.97.

  P1  Diagonal: OS24 → OS24 mean AUC (mean of 3 models) 0.62–0.72;
      platinum → platinum 0.52–0.65.
  P2  OS-trained → platinum: mean AUC (OS18 and OS24, 3 models) ≤ 0.58.
  P3  platinum-trained → OS24: mean AUC ≤ 0.60.
  P4  platinum ↔ pfiplat6 off-diagonal within 0.03 of the corresponding diagonal.

DECISION RULE (all quantities = mean over 3 models and 5 repeats):
  ceiling  = AUC(platinum → platinum)
  label    = ceiling − mean[AUC(OS18 → platinum), AUC(OS24 → platinum)]
  platform = ceiling − 0.589 (A4: platinum-trained, GEO dfs label)
  If ceiling < 0.55: "platinum status is not predictable from expression within
    TCGA at this sample size; label and platform effects cannot be separated".
  Otherwise: label mismatch supported if label ≥ 0.05; platform/cohort shift
    supported if platform ≥ 0.05 (both can hold).
"""
import argparse, sys
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
import sklearn
from sklearn.base import clone
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.data_loader import load_expression
from src.models import get_all_models
from src.preprocessing import clean_expression

EXT = ROOT / "data" / "external"
OUT = ROOT / "label_validity" / "outputs"
LABELS = ["label_platinum", "label_pfiplat6", "label_os18", "label_os24"]
REPEATS, FOLDS, TOPN = 5, 5, 500


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(ROOT / "config" / "config.yaml"))
    expr = clean_expression(load_expression(a.data_dir, cfg["data"]["expression_file"]))
    expr = expr[~expr.index.duplicated()]
    geo = pd.read_csv(EXT / "GSE63885_expr_gene.csv", index_col=0, usecols=[0])
    common = sorted(set(expr.index) & set(geo.index[~geo.index.duplicated()]))

    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    m = m[m["in_rnaseq"]]
    ids = sorted(set(m.index) & set(expr.columns))
    m = m.loc[ids]
    X = np.log2(expr.loc[common, ids].T + 1)                      # patients × genes, log2
    strata = m["label_platinum"].fillna(-1).astype(int).values
    models = get_all_models(cfg)
    print(f"sklearn {sklearn.__version__} | patients {len(ids)} | common genes {len(common)}")
    for l in LABELS:
        print(f"  {l}: determinate {int(m[l].notna().sum())}, label=1 {int((m[l] == 1).sum())}")

    rows = []
    for rep in range(REPEATS):
        oof = {(tl, mn): pd.Series(np.nan, index=ids) for tl in LABELS for mn in models}
        skf = StratifiedKFold(n_splits=FOLDS, shuffle=True, random_state=rep)
        for tr_idx, te_idx in skf.split(ids, strata):
            tr_ids, te_ids = [ids[i] for i in tr_idx], [ids[i] for i in te_idx]
            for tl in LABELS:
                y_tr = m.loc[tr_ids, tl].dropna().astype(int)
                Xtr = X.loc[y_tr.index]
                genes = Xtr.var(axis=0).nlargest(TOPN).index
                sc = StandardScaler().fit(Xtr[genes])
                A, B = sc.transform(Xtr[genes]), sc.transform(X.loc[te_ids, genes])
                for mn, base in models.items():
                    mdl = clone(base).fit(A, y_tr.values)
                    oof[(tl, mn)].loc[te_ids] = mdl.predict_proba(B)[:, 1]
        for (tl, mn), s in oof.items():
            for te in LABELS:
                yt = m[te].dropna().astype(int)
                rows.append(dict(repeat=rep, train_label=tl, test_label=te, model=mn,
                                 n=len(yt), n_pos=int(yt.sum()),
                                 auc=roc_auc_score(yt.values, s.loc[yt.index].values)))
        print(f"repeat {rep} done")
    r = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    r.to_csv(OUT / "a5_cross_label_repeats.csv", index=False)

    per_model = r.groupby(["train_label", "test_label", "model"]).auc.agg(["mean", "min", "max"]).reset_index()
    mean3 = r.groupby(["train_label", "test_label"]).auc.mean().unstack().reindex(index=LABELS, columns=LABELS)

    def A(tr, te):
        return float(mean3.loc[tr, te])

    ceiling = A("label_platinum", "label_platinum")
    label_eff = ceiling - np.mean([A("label_os18", "label_platinum"), A("label_os24", "label_platinum")])
    platform_eff = ceiling - 0.589
    if ceiling < 0.55:
        dec = ("Platinum status is not predictable from expression within TCGA at this sample size; "
               "label and platform effects cannot be separated")
    else:
        parts = []
        parts.append("label mismatch SUPPORTED" if label_eff >= 0.05 else "label mismatch not supported")
        parts.append("platform/cohort shift SUPPORTED" if platform_eff >= 0.05 else "platform/cohort shift not supported")
        dec = "; ".join(parts)

    L = ["# A5 — within-TCGA cross-label prediction", "",
         f"sklearn {sklearn.__version__}; {len(ids)} platinum-treated patients with RNA-seq; {len(common)} common genes; "
         f"{REPEATS} × {FOLDS}-fold CV, pooled out-of-fold AUC per repeat. Variant P preprocessing (as A4).", "",
         "## Mean AUC over 3 models × 5 repeats (rows = training label, columns = test label)", "",
         "```", mean3.round(3).to_string(), "```", "",
         "## Per model: mean [min, max] over repeats", "",
         "```", per_model.round(3).to_string(index=False), "```", "",
         "## Predictions vs observed", "",
         f"- P1 diagonal: OS24→OS24 {A('label_os24','label_os24'):.3f} (predicted 0.62–0.72); "
         f"platinum→platinum {ceiling:.3f} (predicted 0.52–0.65)",
         f"- P2 OS-trained → platinum: OS18 {A('label_os18','label_platinum'):.3f}, OS24 {A('label_os24','label_platinum'):.3f}, "
         f"mean {np.mean([A('label_os18','label_platinum'), A('label_os24','label_platinum')]):.3f} (predicted ≤ 0.58)",
         f"- P3 platinum → OS24: {A('label_platinum','label_os24'):.3f} (predicted ≤ 0.60)",
         f"- P4 platinum→pfiplat6 {A('label_platinum','label_pfiplat6'):.3f} vs pfiplat6→pfiplat6 {A('label_pfiplat6','label_pfiplat6'):.3f}; "
         f"pfiplat6→platinum {A('label_pfiplat6','label_platinum'):.3f} vs platinum→platinum {ceiling:.3f} (predicted within 0.03)",
         "", f"Ceiling {ceiling:.3f}; label effect {label_eff:+.3f}; platform effect {platform_eff:+.3f} (vs A4 GEO dfs 0.589).",
         f"**Decision rule: {dec}.**"]
    (OUT / "05_cross_label_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
