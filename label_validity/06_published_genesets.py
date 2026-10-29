"""
label_validity/06_published_genesets.py
───────────────────────────────────────
Q2 analysis A6 (supplementary) — published gene sets as fixed inputs
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, optional A6; Aaron chose to run it 2026-10-29).

Question: used as fixed inputs to this project's leakage-free pipeline, do two
published platinum-response gene sets predict platinum status better than
random gene sets of the same size?
FRAMING (fixed): this evaluates the gene LISTS as fixed inputs to OUR pipeline.
It is not a reproduction of either paper's pipeline (both are under-specified)
and says nothing about the original authors' reported performance.

Gene sets (verified from the local PDFs, 2026-10-29)
  Chen et al. 2022, J Ovarian Res 15:39, Discussion: "The classifier comprised of 10 genes
    (CD209, CD274, HIST1H3I, HIST1H4L, NLGN1, NTRK3, PNLDC1, SLC22A3, SLC5A1 and SYNM)".
  Gao et al. 2025, Sci Rep 15:19123, Abstract: "5 genes (PAX2, TFPI2, APOA1, ADIRF and CRISP3)".
Symbol mapping (HGNC records, checked 2026-10-29): HIST1H3I = H3C11, HIST1H4L = H4C13
  (GSE63885 file uses the new symbols; TCGA the old); ADIRF previous symbol C10orf116
  (TCGA uses C10orf116, GSE63885 ADIRF). All 15 genes are present on both platforms.

DESIGN (fixed before running)
  Training labels: label_platinum (primary), label_pfiplat6 (secondary), from labels_master.csv,
    platinum-treated patients with RNA-seq.
  Preprocessing (as A4/A5 variant P): TCGA log2(RSEM + 1); StandardScaler fit on training rows
    only; GSE63885 genes z-scored within GEO. No gene selection — the set IS the feature set.
  Endpoints:
    E1  within TCGA: StratifiedKFold(5, shuffle) on patients with the label determinate,
        5 repeats (seeds 0–4); pooled out-of-fold AUC per repeat; mean over repeats.
    E2  transfer: train on all labelled TCGA patients; AUC on GSE63885 dfs label
        (34 resistant / 40 sensitive) — primary transfer endpoint, as in A4.
    E3  transfer: as E2, GSE63885 clinical label (10 / 64) — secondary.
  Null: 1,000 random gene sets per set size (10 and 5) drawn without replacement from the
    symbols common to both platforms that have no missing values in either matrix for the
    patients/samples used (seed 2026; restriction added after a 20-draw VM smoke test hit NaN
    expression values, before any real run); the same random sets are used for
    every label and endpoint; same folds as the published sets.
  Model for the null comparison: Logistic Regression from config/config.yaml (seed 42).
  Random Forest and SVM are reported for the published sets only (descriptive, no null).
  Empirical one-sided p = (1 + #random AUC ≥ published AUC) / 1001.
  Multiplicity: Benjamini–Hochberg across the 12 tests (2 sets × 2 labels × 3 endpoints).

Run on the host (sklearn 1.9.0), from the project root:
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\06_published_genesets.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Outputs → label_validity/outputs/a6_published_sets.csv, a6_null.csv, 06_published_genesets_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Design facts behind them (stated, not judged): Chen et al. selected their 10 genes on TCGA-OV
patients labelled by PFI < 6 months (n = 230), using the full labelled set; those patients very
likely overlap ours (patient IDs not published, overlap not verifiable). Gao et al. took
candidate genes from an external single-cell dataset; the gene count was chosen on pooled
TCGA + GEO data. A5 ceiling for platinum status with 500 variance-selected genes: 0.634.

  P1  Chen set, E1, label_platinum: empirical p < 0.05 (the genes were chosen on overlapping
      TCGA patients, so within-TCGA evaluation is expected to look better than random).
  P2  Chen set, E2 (GEO dfs), label_platinum: empirical p ≥ 0.05.
  P3  Gao set, E1, label_platinum: empirical p ≥ 0.05.
  P4  Gao set, E2, label_platinum: empirical p ≥ 0.05.
  P5  Median random-set E1 AUC (LR, label_platinum): 0.50–0.58 for both set sizes.
  P6  No published-set LR AUC on any endpoint exceeds 0.75.

DECISION RULE: a published set "predicts better than random gene sets of the same size" on an
endpoint only if BH q < 0.05. Otherwise it is reported as "not distinguishable from random gene
sets of the same size under this evaluation".
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
N_NULL, NULL_SEED, REPEATS, FOLDS = 1000, 2026, 5, 5
LABELS = ["label_platinum", "label_pfiplat6"]
# (TCGA symbol, GSE63885 symbol)
SETS = {
    "Chen2022_10": [("CD209", "CD209"), ("CD274", "CD274"), ("HIST1H3I", "H3C11"), ("HIST1H4L", "H4C13"),
                    ("NLGN1", "NLGN1"), ("NTRK3", "NTRK3"), ("PNLDC1", "PNLDC1"), ("SLC22A3", "SLC22A3"),
                    ("SLC5A1", "SLC5A1"), ("SYNM", "SYNM")],
    "Gao2025_5": [("PAX2", "PAX2"), ("TFPI2", "TFPI2"), ("APOA1", "APOA1"), ("C10orf116", "ADIRF"),
                  ("CRISP3", "CRISP3")],
}


def zscore_within(df):
    sd = df.std(axis=0, ddof=0).replace(0, np.nan)
    return ((df - df.mean(axis=0)) / sd).fillna(0.0)


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    q = np.empty(n); q[o] = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
    return np.minimum(q, 1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(ROOT / "config" / "config.yaml"))
    expr = clean_expression(load_expression(a.data_dir, cfg["data"]["expression_file"]))
    expr = expr[~expr.index.duplicated()]
    geo = pd.read_csv(EXT / "GSE63885_expr_gene.csv", index_col=0)
    geo = geo[~geo.index.duplicated()]
    meta = pd.read_csv(EXT / "harmonised_metadata.csv").set_index("sample_id")
    meta = meta.loc[[s for s in geo.columns if s in meta.index]]
    glab = {"E2_geo_dfs": pd.to_numeric(meta["platinum_label_dfs.y"], errors="coerce"),
            "E3_geo_clinical": pd.to_numeric(meta["platinum_label_clinical"], errors="coerce")}
    common = sorted(set(expr.index) & set(geo.index))
    for s, pairs in SETS.items():
        miss = [p for p in pairs if p[0] not in expr.index or p[1] not in geo.index]
        if miss:
            raise SystemExit(f"{s}: genes missing after mapping {miss}")

    m = pd.read_csv(OUT / "labels_master.csv", index_col=0)
    m = m[m["in_rnaseq"]]
    ids = sorted(set(m.index) & set(expr.columns))
    m = m.loc[ids]
    T = np.log2(expr[ids].T + 1)                       # patients × genes (all genes)
    G = zscore_within(geo.T)                            # GEO samples × genes
    complete = [g for g in common if T[g].notna().all() and geo.loc[g].notna().all()]
    for s, pairs in SETS.items():
        bad = [p for p in pairs if T[p[0]].isna().any() or geo.loc[p[1]].isna().any()]
        if bad:
            raise SystemExit(f"{s}: missing expression values for {bad}")
    print(f"null pool: {len(complete)} of {len(common)} common genes have complete data")
    common = complete
    models = get_all_models(cfg)
    lr = models["Logistic Regression"]
    print(f"sklearn {sklearn.__version__} | patients {len(ids)} | common genes {len(common)}")

    folds = {}
    for lab in LABELS:
        y = m[lab].dropna().astype(int)
        folds[lab] = (y, [list(StratifiedKFold(FOLDS, shuffle=True, random_state=r).split(y.index, y.values))
                          for r in range(REPEATS)])

    def evaluate(tg, gg, model, lab):
        y, splits = folds[lab]
        X = T.loc[y.index, tg].values
        e1 = []
        for sp in splits:
            oof = np.empty(len(y))
            for tr, te in sp:
                sc = StandardScaler().fit(X[tr])
                oof[te] = clone(model).fit(sc.transform(X[tr]), y.values[tr]).predict_proba(sc.transform(X[te]))[:, 1]
            e1.append(roc_auc_score(y.values, oof))
        sc = StandardScaler().fit(X)
        mdl = clone(model).fit(sc.transform(X), y.values)
        prob = mdl.predict_proba(G[gg].values)[:, 1]
        out = {"E1_tcga_cv": float(np.mean(e1))}
        for k, yl in glab.items():
            ok = yl.notna().values
            out[k] = roc_auc_score(yl[ok].astype(int).values, prob[ok])
        return out

    rows = []
    for s, pairs in SETS.items():
        tg, gg = [p[0] for p in pairs], [p[1] for p in pairs]
        for lab in LABELS:
            for mn, mdl in models.items():
                for ep, auc in evaluate(tg, gg, mdl, lab).items():
                    rows.append(dict(gene_set=s, size=len(pairs), label=lab, model=mn, endpoint=ep, auc=auc))
        print(f"{s} done")
    pub = pd.DataFrame(rows)

    rng = np.random.default_rng(NULL_SEED)
    null_rows = []
    for size in sorted({len(p) for p in SETS.values()}):
        for i in range(N_NULL):
            genes = list(rng.choice(common, size=size, replace=False))
            for lab in LABELS:
                for ep, auc in evaluate(genes, genes, lr, lab).items():
                    null_rows.append(dict(size=size, draw=i, label=lab, endpoint=ep, auc=auc))
            if (i + 1) % 100 == 0:
                print(f"null size {size}: {i + 1}/{N_NULL}")
    null = pd.DataFrame(null_rows)

    OUT.mkdir(parents=True, exist_ok=True)
    pub.to_csv(OUT / "a6_published_sets.csv", index=False)
    null.to_csv(OUT / "a6_null.csv", index=False)

    tests = []
    for r in pub[pub.model == "Logistic Regression"].itertuples():
        nd = null[(null["size"] == r.size) & (null.label == r.label) & (null.endpoint == r.endpoint)].auc.values
        tests.append(dict(gene_set=r.gene_set, label=r.label, endpoint=r.endpoint, auc_lr=r.auc,
                          null_median=float(np.median(nd)), null_p95=float(np.percentile(nd, 95)),
                          n_null=len(nd), p_emp=(1 + int((nd >= r.auc).sum())) / (1 + len(nd))))
    tests = pd.DataFrame(tests)
    tests["q_bh"] = bh(tests.p_emp.values)
    tests["better_than_random"] = tests.q_bh < 0.05
    tests.to_csv(OUT / "a6_tests.csv", index=False)

    def t(s, lab, ep):
        return tests[(tests.gene_set == s) & (tests.label == lab) & (tests.endpoint == ep)].iloc[0]

    def ft(r):
        return f"AUC {r.auc_lr:.3f} vs random median {r.null_median:.3f} (95th pct {r.null_p95:.3f}), p = {r.p_emp:.3f}, q = {r.q_bh:.3f}"

    desc = pub.pivot_table(index=["gene_set", "label", "model"], columns="endpoint", values="auc")
    L = ["# A6 — published gene sets as fixed inputs (supplementary)", "",
         f"sklearn {sklearn.__version__}; {len(ids)} platinum-treated patients with RNA-seq; null = {N_NULL} random "
         f"same-size sets from {len(common)} common genes. Evaluates the gene LISTS in this pipeline; not a "
         "reproduction of either paper's pipeline.", "",
         "## LR vs random gene sets (BH across 12 tests)", "",
         "```", tests.round(3).to_string(index=False), "```", "",
         "## All models, published sets only (descriptive)", "",
         "```", desc.round(3).to_string(), "```", "",
         "## Predictions vs observed", "",
         f"- P1 Chen, E1, platinum: {ft(t('Chen2022_10','label_platinum','E1_tcga_cv'))} (predicted p < 0.05)",
         f"- P2 Chen, E2, platinum: {ft(t('Chen2022_10','label_platinum','E2_geo_dfs'))} (predicted p ≥ 0.05)",
         f"- P3 Gao, E1, platinum: {ft(t('Gao2025_5','label_platinum','E1_tcga_cv'))} (predicted p ≥ 0.05)",
         f"- P4 Gao, E2, platinum: {ft(t('Gao2025_5','label_platinum','E2_geo_dfs'))} (predicted p ≥ 0.05)",
         "- P5 random-set median E1 AUC, platinum: " + ", ".join(
             f"size {sz} {np.median(null[(null['size'] == sz) & (null.label == 'label_platinum') & (null.endpoint == 'E1_tcga_cv')].auc):.3f}"
             for sz in sorted(null['size'].unique())) + " (predicted 0.50–0.58)",
         f"- P6 max published-set LR AUC on any endpoint: {pub[pub.model == 'Logistic Regression'].auc.max():.3f} (predicted ≤ 0.75)",
         "", "## Decision rule (BH q < 0.05)", ""]
    L += [f"- {r.gene_set} / {r.label} / {r.endpoint}: "
          + ("**better than random gene sets of the same size**" if r.better_than_random
             else "not distinguishable from random gene sets of the same size")
          for r in tests.itertuples()]
    (OUT / "06_published_genesets_summary.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
