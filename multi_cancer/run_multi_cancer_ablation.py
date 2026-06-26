# multi_cancer/run_multi_cancer_ablation.py  (v2)
# Changes from v1:
#   - BRCA dropped (n=32 platinum patients; not standard-of-care)
#   - Cancer-appropriate thresholds per dataset
#   - Pre-patches RSEM file to dedup gene symbols before ablation runs
#   - Adds minimum cohort size check
# Run from project root:
#   python multi_cancer\run_multi_cancer_ablation.py

import subprocess
import sys
import shutil
import yaml
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_BASE    = Path("D:/ALIENWARE/WORK DATA/George Mason/Course Work/"
                    "3rd Sem FALL 2025/BINF 760 ML/Project data")
MC_OUT       = PROJECT_ROOT / "multi_cancer" / "outputs"
MC_OUT.mkdir(parents=True, exist_ok=True)

# ── Cancer studies (BRCA dropped — only 32 platinum patients) ─────────────────
CANCERS = [
    {
        "label":      "LUAD",
        "study_id":   "luad_tcga_pan_can_atlas_2018",
        "name":       "Lung Adenocarcinoma",
        "thresholds": [12, 18, 24],   # same as OV; 146 platinum patients
    },
    {
        "label":      "COADREAD",
        "study_id":   "coadread_tcga_pan_can_atlas_2018",
        "name":       "Colorectal Adenocarcinoma",
        "thresholds": [18, 24, 36],   # 12m only 16 pos; use 18/24/36
        # Pipeline uses exact match on AGENT field — must list every
        # oxaliplatin-containing regimen string that appears in the data
        "platinum_drugs": [
            "OXALIPLATIN",
            "LEUCOVORIN + FLUOROURACIL + OXALIPLATIN",
            "LEUCOVORIN + OXALIPLATIN + FLUOROURACIL + DEXAMETHASONE",
            "OXALIPLATIN + FLUOROURACIL",
            "CISPLATIN",
        ],
    },
]

# ── Load base OV config ───────────────────────────────────────────────────────
base_config_path = PROJECT_ROOT / "config" / "config.yaml"
with open(base_config_path) as f:
    base_config = yaml.safe_load(f)

print("=" * 60)
print("MULTI-CANCER ABLATION RUNNER  (v2)")
print("=" * 60)
print(f"Cancers: {[c['label'] for c in CANCERS]}")
print(f"Note: BRCA dropped (n=32 platinum patients; not standard-of-care)")
print()

# ── Helper: dedup RSEM gene symbols in-place in a temp copy ──────────────────
def make_deduped_rsem(data_dir: Path, tmp_dir: Path) -> Path:
    """
    Copy data_mrna_seq_v2_rsem.txt to tmp_dir with duplicate gene rows removed.
    Returns path to the deduplicated file.
    OV pipeline already handles this internally, but some dependency versions
    now enforce unique column names at load time — pre-deduping avoids the crash.
    """
    src  = data_dir / "data_mrna_seq_v2_rsem.txt"
    dest = tmp_dir / "data_mrna_seq_v2_rsem.txt"

    if dest.exists():
        print(f"  Deduped RSEM already exists: {dest.name}")
        return dest

    print(f"  Reading RSEM for dedup (~30s)...")
    df = pd.read_csv(src, sep="\t", comment="#", header=0, low_memory=False)

    # First column is Hugo_Symbol
    gene_col = df.columns[0]
    before   = len(df)
    df = df[~df[gene_col].duplicated(keep="first")]
    df = df[df[gene_col].notna()]          # drop NaN gene rows
    after = len(df)
    print(f"  Dedup: {before} → {after} genes (removed {before - after} rows)")

    # Fill NaN expression values with 0 (standard for RSEM zero counts)
    expr_cols = df.columns[2:]
    nan_before = df[expr_cols].isna().sum().sum()
    if nan_before > 0:
        df[expr_cols] = df[expr_cols].fillna(0)
        print(f"  NaN fill: replaced {nan_before} NaN expression values with 0")

    dest.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(dest, sep="\t", index=False)
    print(f"  Deduped RSEM saved: {dest}")
    return dest


results_summary = []

for cancer in CANCERS:
    label      = cancer["label"]
    study_id   = cancer["study_id"]
    data_dir   = DATA_BASE / study_id
    thresholds = cancer["thresholds"]

    print(f"\n{'='*60}")
    print(f"CANCER: {label} ({cancer['name']})")
    print(f"Thresholds: {thresholds}m")
    print(f"{'='*60}")

    # Verify data
    rsem_path = data_dir / "data_mrna_seq_v2_rsem.txt"
    if not rsem_path.exists():
        print(f"  ERROR: RSEM not found: {rsem_path}")
        results_summary.append({"cancer": label, "status": "SKIPPED - data missing"})
        continue

    # Output dirs
    cancer_out = MC_OUT / label
    cancer_out.mkdir(parents=True, exist_ok=True)
    (cancer_out / "figures").mkdir(exist_ok=True)
    (cancer_out / "models").mkdir(exist_ok=True)
    (cancer_out / "results").mkdir(exist_ok=True)

    # Deduped data dir (temp copy with RSEM fixed)
    tmp_data_dir = MC_OUT / f"_tmp_{label}_data"
    tmp_data_dir.mkdir(parents=True, exist_ok=True)

    # Symlink / copy all non-RSEM files so pipeline can find them
    for src_file in data_dir.iterdir():
        if src_file.is_dir():
            continue  # skip subdirectories (e.g. case_lists)
        if src_file.name == "data_mrna_seq_v2_rsem.txt":
            continue  # will be replaced by deduped version
        dst_file = tmp_data_dir / src_file.name
        if not dst_file.exists():
            shutil.copy2(src_file, dst_file)

    # Write deduped RSEM
    make_deduped_rsem(data_dir, tmp_data_dir)

    # Build config
    cancer_config = yaml.safe_load(yaml.dump(base_config))
    cancer_config["project"]["name"] = f"{label} Platinum Response"
    cancer_config["data"]["data_dir"] = str(tmp_data_dir).replace("\\", "/")
    cancer_config["clinical"]["thresholds"] = thresholds
    if "platinum_drugs" in cancer:
        cancer_config["clinical"]["platinum_drugs"] = cancer["platinum_drugs"]
    cancer_config["output"]["figures_dir"] = str(cancer_out / "figures").replace("\\", "/")
    cancer_config["output"]["models_dir"]  = str(cancer_out / "models").replace("\\", "/")
    cancer_config["output"]["results_dir"] = str(cancer_out / "results").replace("\\", "/")

    tmp_config = PROJECT_ROOT / "config" / f"config_{label.lower()}_tmp.yaml"
    with open(tmp_config, "w") as f:
        yaml.dump(cancer_config, f, default_flow_style=False)
    print(f"  Config written: {tmp_config.name}")

    # Run ablation
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "run_ablation_study.py"),
        "--config",    str(tmp_config),
        "--n-repeats", "30",
        "--log-level", "WARNING",
    ]
    print(f"  Running ablation (30 splits × {len(thresholds)} thresholds × 3 models × 2 conditions)...")

    log_path = cancer_out / "ablation_run.log"
    try:
        with open(log_path, "w") as log_f:
            result = subprocess.run(
                cmd, cwd=str(PROJECT_ROOT),
                stdout=log_f, stderr=subprocess.STDOUT,
                timeout=3600,
            )
        if result.returncode == 0:
            print(f"  ✓ Complete (returncode=0)")
            status = "SUCCESS"
        else:
            print(f"  ✗ Failed (returncode={result.returncode})")
            with open(log_path) as lf:
                lines = lf.readlines()
            print("  Last 25 log lines:")
            for line in lines[-25:]:
                print(f"    {line.rstrip()}")
            status = f"FAILED (rc={result.returncode})"
    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout")
        status = "TIMEOUT"
    except Exception as e:
        print(f"  ✗ Error: {e}")
        status = f"ERROR: {e}"

    # Cleanup
    tmp_config.unlink(missing_ok=True)

    # Check outputs
    found = [f for f in [
        "ablation_supervised_leakage_summary.csv",
        "ablation_supervised_leakage_raw.csv",
        "ablation_leakage_summary.csv",
        "ablation_leakage_raw.csv",
    ] if (cancer_out / "results" / f).exists()]
    print(f"  Output files: {found}")

    results_summary.append({
        "cancer": label, "status": status, "outputs": found
    })

print(f"\n{'='*60}")
print("RUN SUMMARY")
print(f"{'='*60}")
print(f"  BRCA: SKIPPED (n=32 platinum patients; not standard-of-care for breast cancer)")
for r in results_summary:
    print(f"  {r['cancer']:10s}  {r['status']}")
    for o in r.get("outputs", []):
        print(f"               ✓ {o}")
print(f"\nNext: python multi_cancer\\compare_ablation_results.py")
