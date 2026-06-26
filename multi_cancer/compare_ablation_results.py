# multi_cancer/compare_ablation_results.py  (v2)
# Builds cross-cancer leakage comparison table from ablation_supervised_leakage_summary.csv
# Run from project root:
#   python multi_cancer\compare_ablation_results.py

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MC_OUT       = PROJECT_ROOT / "multi_cancer" / "outputs"
OV_RESULTS   = PROJECT_ROOT / "outputs" / "results"
COMPARE_OUT  = MC_OUT / "comparison"
COMPARE_OUT.mkdir(parents=True, exist_ok=True)

CANCERS = {
    "OV":       {"results_dir": OV_RESULTS,                   "name": "Ovarian (HGSOC)",      "thresholds": [12, 18, 24]},
    "LUAD":     {"results_dir": MC_OUT / "LUAD"     / "results", "name": "Lung Adeno",         "thresholds": [12, 18, 24]},
    "COADREAD": {"results_dir": MC_OUT / "COADREAD" / "results", "name": "Colorectal",         "thresholds": [18, 24, 36]},
}

# ── Load supervised leakage summary for each cancer ───────────────────────────
print("=" * 64)
print("CROSS-CANCER FEATURE SELECTION LEAKAGE — RESULTS")
print("=" * 64)

all_dfs = []
for label, meta in CANCERS.items():
    path = meta["results_dir"] / "ablation_supervised_leakage_summary.csv"
    if not path.exists():
        print(f"  [{label}] MISSING: {path}")
        continue
    df = pd.read_csv(path)
    df["cancer"]      = label
    df["cancer_name"] = meta["name"]
    all_dfs.append(df)
    print(f"  [{label}] Loaded: {len(df)} rows")

combined = pd.concat(all_dfs, ignore_index=True)

# Also load unsupervised (variance) results for comparison
unsup_dfs = []
for label, meta in CANCERS.items():
    path = meta["results_dir"] / "ablation_leakage_summary.csv"
    if not path.exists():
        continue
    df = pd.read_csv(path)
    df["cancer"]      = label
    df["cancer_name"] = meta["name"]
    unsup_dfs.append(df)

unsup_combined = pd.concat(unsup_dfs, ignore_index=True) if unsup_dfs else pd.DataFrame()

# ── Per-cancer summary ────────────────────────────────────────────────────────
print(f"\n{'─'*64}")
print("SUPERVISED F-SCORE LEAKAGE (mean AUC inflation across thresholds & models)")
print(f"{'─'*64}")

summary_rows = []
for label, meta in CANCERS.items():
    sub = combined[combined["cancer"] == label]
    if sub.empty:
        continue

    mean_inf  = sub["auc_inflation"].mean()
    max_inf   = sub["auc_inflation"].max()
    min_inf   = sub["auc_inflation"].min()

    # Which model×threshold has highest inflation
    max_row = sub.loc[sub["auc_inflation"].idxmax()]

    # Unsupervised comparison
    if not unsup_combined.empty:
        unsub = unsup_combined[unsup_combined["cancer"] == label]
        # Column name may differ — find the inflation column
        inf_col = [c for c in unsub.columns if "inflation" in c.lower()]
        unsup_mean = unsub[inf_col[0]].mean() if inf_col else np.nan
    else:
        unsup_mean = np.nan

    summary_rows.append({
        "Cancer":          meta["name"],
        "N_combos":        len(sub),
        "Sup_mean_inf":    round(mean_inf, 4),
        "Sup_max_inf":     round(max_inf, 4),
        "Sup_min_inf":     round(min_inf, 4),
        "Unsup_mean_inf":  round(unsup_mean, 4) if not np.isnan(unsup_mean) else "N/A",
        "Worst_case":      f"{max_row['model']}@{int(max_row['threshold_m'])}m",
    })

    print(f"\n  {meta['name']} ({label}):")
    print(f"    Supervised mean inflation : {mean_inf:+.4f}")
    print(f"    Supervised max inflation  : {max_inf:+.4f}  ({max_row['model']}@{int(max_row['threshold_m'])}m)")
    print(f"    Supervised min inflation  : {min_inf:+.4f}")
    print(f"    Unsupervised mean inflation: {unsup_mean:+.4f}" if not np.isnan(unsup_mean) else "    Unsupervised: N/A")

# ── Full per-model×threshold table ────────────────────────────────────────────
print(f"\n{'─'*64}")
print("PER-MODEL × THRESHOLD LEAKAGE TABLE (supervised AUC inflation)")
print(f"{'─'*64}")

pivot = combined.pivot_table(
    index=["model", "threshold_m"],
    columns="cancer_name",
    values="auc_inflation",
    aggfunc="mean"
).round(4)

# Reorder columns
col_order = [m["name"] for m in CANCERS.values() if m["name"] in pivot.columns]
pivot = pivot[col_order]
print(pivot.to_string())

# ── Paper-ready summary table ─────────────────────────────────────────────────
print(f"\n{'─'*64}")
print("PAPER-READY SUMMARY TABLE")
print(f"{'─'*64}")
summary_df = pd.DataFrame(summary_rows)
print(summary_df.to_string(index=False))

# ── Save outputs ──────────────────────────────────────────────────────────────
pivot.to_csv(COMPARE_OUT / "cross_cancer_leakage_by_model.csv")
summary_df.to_csv(COMPARE_OUT / "cross_cancer_leakage_summary.csv", index=False)
combined.to_csv(COMPARE_OUT / "all_cancers_ablation_raw.csv", index=False)
print(f"\nOutputs saved to: {COMPARE_OUT}")
print("Done. Paste full output into chat.")
