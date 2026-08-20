# phase2/phase2_04b_pathway_enrichment_shap.py
# Purpose: Run the exact same Enrichr pathway enrichment methodology as
#          phase2_04_pathway_enrichment.py, but on the SHAP-based gene lists
#          from phase2_03d (cv_topN_genes_shap_{with12m,without12m}.txt)
#          instead of the original MDI-based lists. SHAP was chosen as the
#          final Finding 5 importance method (converges with MDI at rho=0.98
#          under fair CV comparison; directly addresses Lockhart's MDI-bias
#          comment).
#
# Does NOT modify phase2_04_pathway_enrichment.py, phase2_03/03b/03c/03d,
# config.yaml, .git, or PROJECT_LOG.md. New file only. Original MDI
# enrichment results (enrichment_results_full.csv /
# enrichment_results_significant.csv) are read for reference/comparison
# only - never rewritten.
#
# Run from project root:
#   python phase2\phase2_04b_pathway_enrichment_shap.py

import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE2_OUT = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

ENRICHR_BASE = "https://maayanlab.cloud/Enrichr"

# ── Gene lists: SHAP-based, from phase2_03d, both scenarios x all 4 sizes ──
SCENARIOS = ["with12m", "without12m"]
SIZES = [50, 100, 200, 500]

GENE_LIST_FILES = {}
for scenario in SCENARIOS:
    for size in SIZES:
        label = f"SHAP_{scenario}_top{size}"
        GENE_LIST_FILES[label] = dict(
            path=PHASE2_OUT / f"cv_top{size}_genes_shap_{scenario}.txt",
            scenario=scenario,
            size=size,
        )

# Same 4 databases as phase2_04_pathway_enrichment.py (verified by reading
# that script directly before writing this one - not assumed)
DATABASES = [
    "KEGG_2021_Human",
    "Reactome_2022",
    "GO_Biological_Process_2023",
    "MSigDB_Hallmark_2020",
]

# Theme anchor terms, identified from the original MDI enrichment
# (enrichment_results_significant.csv):
#   Theme 2 (ECM/EMT): MSigDB Hallmark "Epithelial Mesenchymal Transition",
#                       KEGG "ECM-receptor interaction", KEGG "Focal adhesion"
#   Theme 1 (ribosome/translation): KEGG "Ribosome" is the cleanest single
#                       cross-database anchor term (also present heavily in
#                       Reactome translation terms, but KEGG Ribosome is the
#                       one comparable term present at top100 AND top200 in
#                       the original run)
THEME_TERMS = [
    ("Theme 2 - ECM/EMT", "MSigDB_Hallmark_2020", "Epithelial Mesenchymal Transition"),
    ("Theme 2 - ECM/EMT", "KEGG_2021_Human", "ECM-receptor interaction"),
    ("Theme 2 - ECM/EMT", "KEGG_2021_Human", "Focal adhesion"),
    ("Theme 1 - Ribosome/Translation", "KEGG_2021_Human", "Ribosome"),
]

SIG_THRESHOLD = 0.05  # same convention as phase2_04_pathway_enrichment.py


def log(msg: str) -> None:
    print(msg, flush=True)


# ── Helper functions (verbatim logic from phase2_04_pathway_enrichment.py,
#    copied rather than reimplemented, to guarantee identical methodology) ──

def enrichr_add_list(genes: list[str], description: str) -> str | None:
    """Upload gene list to Enrichr, return list ID."""
    genes_str = "\n".join(genes)
    payload = {
        "list": (None, genes_str),
        "description": (None, description),
    }
    boundary = "----EnrichrBoundary"
    body = ""
    for key, (_, val) in payload.items():
        body += f"--{boundary}\r\n"
        body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
        body += f"{val}\r\n"
    body += f"--{boundary}--\r\n"
    body_bytes = body.encode("utf-8")

    req = urllib.request.Request(
        f"{ENRICHR_BASE}/addList",
        data=body_bytes,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("userListId")
    except Exception as e:
        log(f"    ERROR uploading gene list: {e}")
        return None


def enrichr_get_results(list_id: str, database: str) -> list | None:
    """Fetch enrichment results for a given list ID and database."""
    url = (f"{ENRICHR_BASE}/enrich?"
           f"userListId={list_id}&backgroundType={urllib.parse.quote(database)}")
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get(database, [])
    except Exception as e:
        log(f"    ERROR fetching {database}: {e}")
        return None


def parse_results(raw: list, database: str) -> pd.DataFrame:
    """
    Enrichr result format (per term):
    [rank, term, p-value, z-score, combined_score, overlapping_genes,
     adjusted_p-value, old_p-value, old_adjusted_p-value]
    """
    if not raw:
        return pd.DataFrame()
    records = []
    for row in raw:
        records.append({
            "database": database,
            "rank": row[0],
            "term": row[1],
            "p_value": row[2],
            "z_score": row[3],
            "combined_score": row[4],
            "overlap_genes": ";".join(row[5]) if isinstance(row[5], list) else row[5],
            "n_overlap": len(row[5]) if isinstance(row[5], list) else None,
            "adj_p_value": row[6],
        })
    return pd.DataFrame(records)


# ── Main loop over the 8 SHAP gene lists ──────────────────────────────────
log("=" * 70)
log("phase2_04b - Pathway enrichment on SHAP-based gene lists (with12m / without12m)")
log("=" * 70)

results_by_scenario = {"with12m": [], "without12m": []}

for list_label, meta in GENE_LIST_FILES.items():
    gene_file = meta["path"]
    scenario = meta["scenario"]
    size = meta["size"]

    if not gene_file.exists():
        log(f"SKIP {list_label}: file not found ({gene_file})")
        continue

    genes = [g.strip() for g in gene_file.read_text().splitlines() if g.strip()]
    log(f"\n{'='*56}")
    log(f"Gene list: {list_label} ({len(genes)} genes)")
    log(f"{'='*56}")

    log("  Uploading to Enrichr...")
    list_id = enrichr_add_list(genes, f"OV_platinum_SHAP_{scenario}_top{size}")
    if list_id is None:
        log(f"  FAILED to upload {list_label} - skipping")
        continue
    log(f"  List ID: {list_id}")
    time.sleep(1)  # be polite to API - same as phase2_04_pathway_enrichment.py

    for db in DATABASES:
        log(f"  Querying {db}...")
        raw = enrichr_get_results(list_id, db)
        time.sleep(0.5)  # same as phase2_04_pathway_enrichment.py

        if raw is None:
            log("    No results returned")
            continue

        df = parse_results(raw, db)
        if df.empty:
            log("    Empty results")
            continue

        df["gene_list"] = list_label
        df["scenario"] = scenario
        df["size"] = size
        df["n_genes_submitted"] = len(genes)
        results_by_scenario[scenario].append(df)

        top5 = df.nsmallest(5, "adj_p_value")
        log("    Top 5 terms (by adj p-value):")
        for _, row in top5.iterrows():
            log(f"      [{row['adj_p_value']:.2e}] {row['term'][:70]}")
            log(f"               overlap={row['n_overlap']}  "
                f"combined_score={row['combined_score']:.1f}")

# ── Save per-scenario full/significant results ─────────────────────────────
log(f"\n{'='*70}")
log("Saving results...")
log(f"{'='*70}")

combined_by_scenario = {}
for scenario in SCENARIOS:
    parts = results_by_scenario[scenario]
    if not parts:
        log(f"ERROR: no enrichment results returned for scenario={scenario}. "
            f"Check internet connection / gene list files.")
        continue
    combined = pd.concat(parts, ignore_index=True)
    combined_by_scenario[scenario] = combined

    full_csv = PHASE2_OUT / f"enrichment_shap_{scenario}_full.csv"
    combined.to_csv(full_csv, index=False)
    log(f"  [{scenario}] Full results: {full_csv.name}  ({len(combined)} terms)")

    sig = combined[combined["adj_p_value"] < SIG_THRESHOLD].copy()
    sig_csv = PHASE2_OUT / f"enrichment_shap_{scenario}_significant.csv"
    sig.to_csv(sig_csv, index=False)
    log(f"  [{scenario}] Significant (adj_p<{SIG_THRESHOLD}): {sig_csv.name}  ({len(sig)} terms)")

if len(combined_by_scenario) < 2:
    log("\nERROR: could not build both scenarios - stopping before comparison table.")
    sys.exit(1)

# ── Load original MDI results for reference (read-only, never rewritten) ──
log(f"\n{'='*70}")
log("Loading original MDI enrichment results for reference (read-only)")
log(f"{'='*70}")
mdi_full_path = PHASE2_OUT / "enrichment_results_full.csv"
mdi_full = pd.read_csv(mdi_full_path)
log(f"  Loaded {mdi_full_path.name}: {mdi_full.shape}, "
    f"gene_list values present: {sorted(mdi_full['gene_list'].unique())}")
# Original script used labels "top50"/"top100"/"top200" with implicit sizes
# 50/100/200 (n_genes_submitted column confirms this)
mdi_full["size"] = mdi_full["n_genes_submitted"]

# ── Build theme comparison table ───────────────────────────────────────────
log(f"\n{'='*70}")
log("BUILDING shap_theme_comparison.csv")
log(f"{'='*70}")

comparison_rows = []

for theme, database, term in THEME_TERMS:
    # Original MDI - whatever sizes were run (50/100/200, no 500)
    mdi_term_rows = mdi_full[(mdi_full["database"] == database) & (mdi_full["term"] == term)]
    for size in [50, 100, 200]:
        match = mdi_term_rows[mdi_term_rows["size"] == size]
        if len(match):
            adj_p = float(match["adj_p_value"].iloc[0])
            n_ov = int(match["n_overlap"].iloc[0])
            found = True
        else:
            adj_p, n_ov, found = None, None, False
        comparison_rows.append(dict(
            theme=theme, database=database, term=term, condition="original-MDI",
            size=size, adj_p_value=adj_p, n_overlap=n_ov,
            significant=(adj_p is not None and adj_p < SIG_THRESHOLD),
            term_returned=found,
        ))
    # original-MDI has no top500 run - record explicitly as not-run, not "not significant"
    comparison_rows.append(dict(
        theme=theme, database=database, term=term, condition="original-MDI",
        size=500, adj_p_value=None, n_overlap=None, significant=False,
        term_returned=False,
    ))

    # SHAP with12m / without12m - all 4 sizes
    for scenario in SCENARIOS:
        combined = combined_by_scenario[scenario]
        term_rows = combined[(combined["database"] == database) & (combined["term"] == term)]
        for size in SIZES:
            match = term_rows[term_rows["size"] == size]
            if len(match):
                adj_p = float(match["adj_p_value"].iloc[0])
                n_ov = int(match["n_overlap"].iloc[0])
                found = True
            else:
                adj_p, n_ov, found = None, None, False
            comparison_rows.append(dict(
                theme=theme, database=database, term=term,
                condition=f"SHAP-{scenario}", size=size,
                adj_p_value=adj_p, n_overlap=n_ov,
                significant=(adj_p is not None and adj_p < SIG_THRESHOLD),
                term_returned=found,
            ))

comparison_df = pd.DataFrame(comparison_rows)
comparison_path = PHASE2_OUT / "shap_theme_comparison.csv"
comparison_df.to_csv(comparison_path, index=False)
log(f"  Saved {comparison_path.name} ({len(comparison_df)} rows)")

# ── Explicit robustness flags (the single most important output) ─────────
log(f"\n{'='*70}")
log("ROBUSTNESS VERDICT: are Finding 5's two headline themes robust to the 12m question?")
log(f"{'='*70}")

verdict_rows = []
for theme in ["Theme 2 - ECM/EMT", "Theme 1 - Ribosome/Translation"]:
    theme_terms = [t for th, db, t in THEME_TERMS if th == theme]
    log(f"\n{theme}:")
    for scenario in SCENARIOS:
        sub = comparison_df[
            (comparison_df["theme"] == theme)
            & (comparison_df["condition"] == f"SHAP-{scenario}")
        ]
        sig_by_size = sub.groupby("size")["significant"].any()
        n_sizes_significant = int(sig_by_size.sum())
        n_sizes_tested = len(sig_by_size)
        robust = n_sizes_significant == n_sizes_tested
        log(f"  SHAP-{scenario}: significant (adj_p<{SIG_THRESHOLD}) in "
            f"{n_sizes_significant}/{n_sizes_tested} sizes tested "
            f"-> {'ROBUST' if robust else 'NOT ROBUST'}")
        for size, is_sig in sig_by_size.items():
            log(f"      top{size}: {'significant' if is_sig else 'NOT significant'}")
        verdict_rows.append(dict(
            theme=theme, condition=f"SHAP-{scenario}",
            n_sizes_significant=n_sizes_significant, n_sizes_tested=n_sizes_tested,
            robust_across_all_sizes=robust,
        ))

verdict_df = pd.DataFrame(verdict_rows)
verdict_path = PHASE2_OUT / "shap_theme_robustness_verdict.csv"
verdict_df.to_csv(verdict_path, index=False)
log(f"\nSaved {verdict_path.name}")

log(f"\n{'='*70}")
log("SUMMARY")
log(f"{'='*70}")
print(verdict_df.to_string(index=False))
log(f"\nOutput files written to: {PHASE2_OUT}")
log("Done. Paste full output into chat.")
