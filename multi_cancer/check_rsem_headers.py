# multi_cancer/check_rsem_headers.py
# Compares column headers between original and deduped COADREAD RSEM files.
# Run from project root:
#   python multi_cancer\check_rsem_headers.py

import pandas as pd
from pathlib import Path

ORIG = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
            "3rd Sem FALL 2025/BINF 760 ML/Project data/"
            "coadread_tcga_pan_can_atlas_2018/data_mrna_seq_v2_rsem.txt")

TMP  = Path("multi_cancer/outputs/_tmp_COADREAD_data/data_mrna_seq_v2_rsem.txt")

def get_headers(path):
    df = pd.read_csv(path, sep="\t", nrows=0)
    return df.columns.tolist()

orig_cols = get_headers(ORIG)
print(f"Original RSEM columns : {len(orig_cols)}")
print(f"  First 5 : {orig_cols[:5]}")
print(f"  Last 2  : {orig_cols[-2:]}")

if TMP.exists():
    tmp_cols = get_headers(TMP)
    print(f"\nDeduped RSEM columns  : {len(tmp_cols)}")
    print(f"  First 5 : {tmp_cols[:5]}")
    print(f"  Last 2  : {tmp_cols[-2:]}")
    print(f"\nFirst col same? {orig_cols[0] == tmp_cols[0]}")
    print(f"Sample cols same? {orig_cols[2:5] == tmp_cols[2:5]}")
else:
    print(f"\nTemp file not found: {TMP}")
    print("Run the ablation runner first to generate it.")

# Also check the OV RSEM for comparison
OV = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
          "3rd Sem FALL 2025/BINF 760 ML/Project data/"
          "ov_tcga_pan_can_atlas_2018/data_mrna_seq_v2_rsem.txt")
ov_cols = get_headers(OV)
print(f"\nOV RSEM columns : {len(ov_cols)}")
print(f"  First 5 : {ov_cols[:5]}")
