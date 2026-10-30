#!/usr/bin/env python3
"""
label_validity/14_cohort_characteristics.py
───────────────────────────────────────────
A14 — descriptive (no predictions): baseline characteristics of the 489 platinum-treated patients and of the
251 with RNA-seq data, for the reporting checklist (STROBE item 14 / STARD item 20). Added 2026-10-29.
Inputs: label_validity/outputs/labels_full.csv, a3_covariates.csv, a8_carriers.csv; ov_tcga_pub case list (sequenced).
Output → label_validity/outputs/a14_cohort_characteristics.csv
Run: python label_validity/14_cohort_characteristics.py --data-root "<...>/OV Data/Project data"
"""
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
O = ROOT / "label_validity" / "outputs"
ap = argparse.ArgumentParser(); ap.add_argument("--data-root", default=str(ROOT.parent / "OV Data" / "Project data"))
dr = Path(ap.parse_args().data_root)
f = pd.read_csv(O / "labels_full.csv", index_col=0).join(pd.read_csv(O / "a3_covariates.csv", index_col=0))
txt = (dr / "ov_tcga_pub" / "ov_tcga_pub" / "case_lists" / "cases_sequenced.txt").read_text(encoding="utf-8")
seq = {x[:12] for x in txt.split("case_list_ids:")[1].split()}
car = pd.read_csv(O / "a8_carriers.csv")
car = set(car[car.trunc.astype(bool) & car.Mutation_Status.isin(["Germline", "Somatic"])].pid)
f["sequenced_2011"] = f.index.isin(seq)
f["brca_carrier"] = f.index.isin(car)
rows = []
for name, d in [("platinum-treated (n = 489)", f), ("with RNA-seq data", f[f.in_rnaseq.astype(bool)])]:
    def cnt(col, val=1):
        s = d[col].dropna(); return f"{int((s == val).sum())}/{len(s)} ({(s == val).mean():.0%})"
    rows += [
        dict(group=name, characteristic="patients", value=str(len(d))),
        dict(group=name, characteristic="age at diagnosis, median (IQR), years",
             value=f"{d.age.median():.0f} ({d.age.quantile(.25):.0f}–{d.age.quantile(.75):.0f}); n {d.age.notna().sum()}"),
        dict(group=name, characteristic="stage IV", value=cnt("stage_iv")),
        dict(group=name, characteristic="residual disease > 1 cm", value=cnt("residual_subopt")),
        dict(group=name, characteristic="Aneuploidy Score, median (IQR)",
             value=f"{d.aneuploidy.median():.0f} ({d.aneuploidy.quantile(.25):.0f}–{d.aneuploidy.quantile(.75):.0f}); n {d.aneuploidy.notna().sum()}"),
        dict(group=name, characteristic="sequenced in 2011 release", value=f"{int(d.sequenced_2011.sum())}"),
        dict(group=name, characteristic="BRCA1/2 carrier (germline or somatic truncating/splice), of sequenced",
             value=f"{int((d.brca_carrier & d.sequenced_2011).sum())}/{int(d.sequenced_2011.sum())}"),
        dict(group=name, characteristic="platinum status determinate", value=cnt("label_platinum", 1).split(" ")[0].split("/")[1] if False else f"{int(d.label_platinum.notna().sum())}"),
    ]
pd.DataFrame(rows).to_csv(O / "a14_cohort_characteristics.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))
