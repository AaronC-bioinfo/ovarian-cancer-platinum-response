# multi_cancer/diagnose_coadread_ids.py
# Purpose: Check why COADREAD patient IDs don't overlap between RSEM and clinical.
# Run from project root:
#   python multi_cancer\diagnose_coadread_ids.py

import pandas as pd
from pathlib import Path

DATA_DIR = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
                "3rd Sem FALL 2025/BINF 760 ML/Project data/"
                "coadread_tcga_pan_can_atlas_2018")

TMP_DIR  = Path("C:/PROJECTS/ovarian-cancer-platinum-response/"
                "multi_cancer/outputs/_tmp_COADREAD_data")

def load_cbio(path):
    return pd.read_csv(path, sep="\t", comment="#", low_memory=False)

# ── Clinical patient IDs ───────────────────────────────────────────────────────
clin = load_cbio(DATA_DIR / "data_clinical_patient.txt")
clin_ids = set(clin["PATIENT_ID"].dropna().tolist())
print(f"Clinical patient IDs: {len(clin_ids)}")
print(f"  Sample: {list(clin_ids)[:5]}")

# ── Treatment platinum patient IDs ────────────────────────────────────────────
trt = load_cbio(DATA_DIR / "data_timeline_treatment.txt")
plat_mask = trt["AGENT"].str.contains("platin", case=False, na=False)
plat_ids  = set(trt.loc[plat_mask, "PATIENT_ID"].dropna().tolist())
print(f"\nPlatinum patient IDs: {len(plat_ids)}")
print(f"  Sample: {list(plat_ids)[:5]}")

# ── RSEM sample IDs (column headers) ─────────────────────────────────────────
# Read from the deduped tmp copy
rsem_path = TMP_DIR / "data_mrna_seq_v2_rsem.txt"
rsem_header = pd.read_csv(rsem_path, sep="\t", nrows=0)
rsem_cols = rsem_header.columns.tolist()
# Drop first two cols (Hugo_Symbol, Entrez_Gene_Id)
sample_cols = [c for c in rsem_cols if c.startswith("TCGA")]
print(f"\nRSEM sample columns: {len(sample_cols)}")
print(f"  Sample: {sample_cols[:5]}")

# ── How does the pipeline derive patient IDs from sample IDs? ─────────────────
# Standard TCGA: sample ID = TCGA-XX-XXXX-01  → patient ID = TCGA-XX-XXXX (first 12 chars)
sample_to_patient = {s: s[:12] for s in sample_cols}
rsem_patient_ids  = set(sample_to_patient.values())
print(f"\nRSEM → patient IDs (first 12 chars): {len(rsem_patient_ids)}")
print(f"  Sample: {list(rsem_patient_ids)[:5]}")

# ── Overlap checks ────────────────────────────────────────────────────────────
overlap_clin  = clin_ids & rsem_patient_ids
overlap_plat  = plat_ids & rsem_patient_ids
print(f"\nOverlap: clinical ∩ RSEM patient IDs = {len(overlap_clin)}")
print(f"Overlap: platinum ∩ RSEM patient IDs  = {len(overlap_plat)}")

if len(overlap_clin) == 0:
    print("\nZERO OVERLAP — checking ID format differences:")
    print(f"  Clinical ID example  : '{list(clin_ids)[0]}'  (len={len(list(clin_ids)[0])})")
    print(f"  RSEM patient ID ex   : '{list(rsem_patient_ids)[0]}'  (len={len(list(rsem_patient_ids)[0])})")
    print(f"  RSEM sample col ex   : '{sample_cols[0]}'")

    # Try longer prefix
    for n in [15, 16, 19]:
        rsem_ids_n = set(s[:n] for s in sample_cols)
        ov2 = clin_ids & rsem_ids_n
        print(f"  Overlap with first {n} chars of sample ID: {len(ov2)}")

print("\nDone.")
