"""
label_validity/04a_rf_determinism_check.py
──────────────────────────────────────────
Diagnostic for A4 check C1 (FAILED 2026-10-29): only Random Forest rows of
04_transfer_matrix.py differed from validation/outputs/external_validation_v2_results.csv
(LR and SVM matched exactly). On the VM (sklearn 1.7.2, Python 3.10) both the
v2 and A4 constructions give RF AUC 0.6312 for 12m / variant S / clinical —
v2's recorded 0.631 — while the host A4 run gave 0.471.

Hypothesis under test: RandomForestClassifier(random_state=42, n_jobs=-1) is
not reproducible run-to-run on the host build. This script fits the SAME RF on
the SAME data six times — three with n_jobs=-1 (as in src/models.py) and three
with n_jobs=1 — and prints the GSE63885 AUC each time, plus the interpreter
build. Nothing in src/ is changed.

Prediction (written before running): if the hypothesis is right, the n_jobs=-1
AUCs differ from each other and the n_jobs=1 AUCs are identical.

Run on the host from the project root:
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\04a_rf_determinism_check.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Output: printed, and label_validity/outputs/04a_rf_determinism.txt
"""
import argparse, sys, platform
from pathlib import Path
import numpy as np
import pandas as pd
import yaml
import sklearn
from sklearn.base import clone
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.data_loader import load_clinical, load_expression, load_treatment
from src.models import get_all_models
from src.preprocessing import (align_expression_to_labels, build_labelled_survival,
                               clean_expression, extract_survival, identify_platinum_patients)


def zscore_within(df):
    sd = df.std(axis=0, ddof=0).replace(0, np.nan)
    return ((df - df.mean(axis=0)) / sd).fillna(0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(ROOT / "config" / "config.yaml"))
    d = a.data_dir
    expr = clean_expression(load_expression(d, cfg["data"]["expression_file"]))
    surv = extract_survival(load_clinical(d, cfg["data"]["clinical_file"]),
                            cfg["clinical"]["time_col"], cfg["clinical"]["status_col"])
    plat = identify_platinum_patients(load_treatment(d, cfg["data"]["treatment_file"]), cfg["clinical"]["platinum_drugs"])
    lab = build_labelled_survival(surv, plat, cfg["clinical"]["time_col"], [12])[12]

    geo = pd.read_csv(ROOT / "data/external/GSE63885_expr_gene.csv", index_col=0)
    meta = pd.read_csv(ROOT / "data/external/harmonised_metadata.csv").set_index("sample_id")
    meta = meta.loc[[s for s in geo.columns if s in meta.index]]
    yg = pd.to_numeric(meta["platinum_label_clinical"], errors="coerce")
    expr = expr[~expr.index.duplicated()]; geo = geo[~geo.index.duplicated()]
    common = sorted(set(expr.index) & set(geo.index))

    X, y = align_expression_to_labels(expr.loc[common], lab)      # variant S (raw RSEM), as in 06
    genes = X.var(axis=0).nlargest(cfg["features"]["top_n_genes"]).index
    Xtr = StandardScaler().fit(X[genes]).transform(X[genes])
    G = zscore_within(geo.loc[genes].T)[genes].values
    m = yg.notna().values; yy = yg[m].astype(int).values

    gil = getattr(sys, "_is_gil_enabled", lambda: "n/a")()
    lines = [f"Python {sys.version.split()[0]} ({platform.python_implementation()}), GIL enabled: {gil}",
             f"sklearn {sklearn.__version__}, numpy {np.__version__}",
             f"12m / variant S / GEO clinical label; TCGA n={len(y)}, events={int(y.sum())}; v2 recorded RF AUC 0.6312", ""]
    base = get_all_models(cfg)["Random Forest"]
    for nj in (-1, -1, -1, 1, 1, 1):
        rf = clone(base).set_params(n_jobs=nj)
        rf.fit(Xtr, y.values)
        auc = roc_auc_score(yy, rf.predict_proba(G)[:, 1][m])
        lines.append(f"n_jobs={nj:>2}  AUC {auc:.4f}")
    out = ROOT / "label_validity" / "outputs" / "04a_rf_determinism.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
