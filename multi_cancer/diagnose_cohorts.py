# multi_cancer/diagnose_cohorts.py
# Purpose: Check platinum-treated cohort sizes and OS distributions for
#          BRCA, LUAD, COADREAD to determine appropriate thresholds.
# Run from project root:
#   python multi_cancer\diagnose_cohorts.py

import pandas as pd
import numpy as np
from pathlib import Path

DATA_BASE = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
                 "3rd Sem FALL 2025/BINF 760 ML/Project data")

CANCERS = {
    "OV":       "ov_tcga_pan_can_atlas_2018",
    "BRCA":     "brca_tcga_pan_can_atlas_2018",
    "LUAD":     "luad_tcga_pan_can_atlas_2018",
    "COADREAD": "coadread_tcga_pan_can_atlas_2018",
}

def load_cbio(path):
    return pd.read_csv(path, sep="\t", comment="#",
                       low_memory=False, na_values=["[Not Available]","NA",""])

for label, study_id in CANCERS.items():
    data_dir = DATA_BASE / study_id
    print(f"\n{'='*60}")
    print(f"CANCER: {label} ({study_id})")
    print(f"{'='*60}")

    # ── Clinical patient file ─────────────────────────────────────────────────
    clin_path = data_dir / "data_clinical_patient.txt"
    if not clin_path.exists():
        print(f"  MISSING: {clin_path}")
        continue
    clin = load_cbio(clin_path)
    print(f"  Clinical: {clin.shape[0]} patients, {clin.shape[1]} cols")

    # OS columns
    os_cols = [c for c in clin.columns if "OS" in c.upper()]
    print(f"  OS-related columns: {os_cols}")

    if "OS_MONTHS" in clin.columns and "OS_STATUS" in clin.columns:
        os_m = pd.to_numeric(clin["OS_MONTHS"], errors="coerce")
        print(f"  OS_MONTHS: n={os_m.notna().sum()}  "
              f"min={os_m.min():.1f}  median={os_m.median():.1f}  "
              f"max={os_m.max():.1f}")
        print(f"  OS_STATUS values: {clin['OS_STATUS'].value_counts().to_dict()}")

    # ── Treatment file ────────────────────────────────────────────────────────
    trt_path = data_dir / "data_timeline_treatment.txt"
    if not trt_path.exists():
        print(f"  MISSING treatment file: {trt_path}")
        # Check alternate names
        alt = list(data_dir.glob("*treatment*")) + list(data_dir.glob("*drug*"))
        print(f"  Alternate files: {[f.name for f in alt]}")
        plat_patients = set()
    else:
        trt = load_cbio(trt_path)
        print(f"  Treatment: {trt.shape[0]} rows")
        if "AGENT" in trt.columns:
            plat_mask = trt["AGENT"].str.contains("platin", case=False, na=False)
            plat_patients = set(trt.loc[plat_mask, "PATIENT_ID"].unique())
            plat_agents = trt.loc[plat_mask, "AGENT"].unique()
            print(f"  Platinum patients: {len(plat_patients)}")
            print(f"  Platinum agents: {list(plat_agents)[:6]}")
        else:
            print(f"  No AGENT column. Columns: {trt.columns.tolist()[:10]}")
            plat_patients = set()

    # ── Platinum subset OS distribution ───────────────────────────────────────
    if plat_patients and "OS_MONTHS" in clin.columns:
        plat_clin = clin[clin["PATIENT_ID"].isin(plat_patients)].copy()
        print(f"\n  Platinum-subset: {len(plat_clin)} patients")
        os_m = pd.to_numeric(plat_clin["OS_MONTHS"], errors="coerce")
        os_s = plat_clin["OS_STATUS"].astype(str)
        print(f"  OS_MONTHS: median={os_m.median():.1f}  "
              f"p25={os_m.quantile(0.25):.1f}  p75={os_m.quantile(0.75):.1f}")

        # Simulate label counts at various thresholds
        print(f"\n  Label counts at each threshold (1=short OS = proxy 'resistant'):")
        print(f"  {'Threshold':>10}  {'N_total':>8}  {'N_pos(1)':>9}  "
              f"{'N_neg(0)':>9}  {'Pct_pos':>8}")
        for t in [12, 18, 24, 36, 48, 60]:
            valid = plat_clin[os_m.notna()].copy()
            valid_os = os_m[os_m.notna()]
            # Standard OS-threshold label: died before threshold = 1
            labels = (valid_os <= t).astype(int)
            n_pos = (labels == 1).sum()
            n_neg = (labels == 0).sum()
            n_tot = len(labels)
            pct   = 100 * n_pos / n_tot if n_tot > 0 else 0
            flag  = " ← too few positives" if n_pos < 5 else ""
            flag  = " ← too few negatives" if n_neg < 5 else flag
            print(f"  {t:>10}m  {n_tot:>8}  {n_pos:>9}  {n_neg:>9}  "
                  f"{pct:>7.1f}%{flag}")

    # ── Check for duplicate gene symbols in RSEM ──────────────────────────────
    rsem_path = data_dir / "data_mrna_seq_v2_rsem.txt"
    if rsem_path.exists():
        # Read only the gene symbol column (first col)
        genes = pd.read_csv(rsem_path, sep="\t", comment="#",
                            usecols=[0], header=0).iloc[:, 0]
        dupes = genes[genes.duplicated()].unique()
        print(f"\n  RSEM duplicate gene symbols: {len(dupes)}")
        if len(dupes) > 0:
            print(f"  Duplicate genes: {list(dupes)[:10]}")

print(f"\n{'='*60}")
print("DIAGNOSIS COMPLETE — paste full output into chat")
print(f"{'='*60}")
