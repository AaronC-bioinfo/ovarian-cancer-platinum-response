# phase2/phase2_04_pathway_enrichment.py
# Purpose: Run pathway enrichment on top RF importance genes via Enrichr API.
#          Queries KEGG_2021_Human, Reactome_2022, GO_Biological_Process_2023
#          No local installation needed — uses Enrichr REST API.
# Run from project root:
#   python phase2\phase2_04_pathway_enrichment.py

import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PHASE2_OUT   = PROJECT_ROOT / "phase2" / "outputs"
PHASE2_OUT.mkdir(parents=True, exist_ok=True)

ENRICHR_BASE = "https://maayanlab.cloud/Enrichr"

# Gene lists to test
GENE_LIST_FILES = {
    "top50":  PHASE2_OUT / "top50_genes_named.txt",
    "top100": PHASE2_OUT / "top100_genes_named.txt",
    "top200": PHASE2_OUT / "top200_genes_named.txt",
}

# Databases to query
DATABASES = [
    "KEGG_2021_Human",
    "Reactome_2022",
    "GO_Biological_Process_2023",
    "MSigDB_Hallmark_2020",
]

# ── Helper functions ───────────────────────────────────────────────────────────

def enrichr_add_list(genes: list[str], description: str) -> str | None:
    """Upload gene list to Enrichr, return list ID."""
    genes_str = "\n".join(genes)
    payload = {
        "list": (None, genes_str),
        "description": (None, description),
    }
    # Build multipart manually for urllib
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
        print(f"    ERROR uploading gene list: {e}")
        return None


def enrichr_get_results(list_id: str, database: str) -> list[dict] | None:
    """Fetch enrichment results for a given list ID and database."""
    url = (f"{ENRICHR_BASE}/enrich?"
           f"userListId={list_id}&backgroundType={urllib.parse.quote(database)}")
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            # Results keyed by database name
            return data.get(database, [])
    except Exception as e:
        print(f"    ERROR fetching {database}: {e}")
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
            "database":        database,
            "rank":            row[0],
            "term":            row[1],
            "p_value":         row[2],
            "z_score":         row[3],
            "combined_score":  row[4],
            "overlap_genes":   ";".join(row[5]) if isinstance(row[5], list) else row[5],
            "n_overlap":       len(row[5]) if isinstance(row[5], list) else None,
            "adj_p_value":     row[6],
        })
    return pd.DataFrame(records)


# ── Main loop ─────────────────────────────────────────────────────────────────
all_results = []

for list_label, gene_file in GENE_LIST_FILES.items():
    if not gene_file.exists():
        print(f"SKIP {list_label}: file not found ({gene_file})")
        continue

    genes = [g.strip() for g in gene_file.read_text().splitlines() if g.strip()]
    print(f"\n{'='*56}")
    print(f"Gene list: {list_label} ({len(genes)} genes)")
    print(f"{'='*56}")

    # Upload list
    print(f"  Uploading to Enrichr...")
    list_id = enrichr_add_list(genes, f"OV_platinum_RF_{list_label}")
    if list_id is None:
        print(f"  FAILED to upload {list_label} — skipping")
        continue
    print(f"  List ID: {list_id}")
    time.sleep(1)  # be polite to API

    # Query each database
    for db in DATABASES:
        print(f"  Querying {db}...")
        raw = enrichr_get_results(list_id, db)
        time.sleep(0.5)

        if raw is None:
            print(f"    No results returned")
            continue

        df = parse_results(raw, db)
        if df.empty:
            print(f"    Empty results")
            continue

        df["gene_list"] = list_label
        df["n_genes_submitted"] = len(genes)
        all_results.append(df)

        # Print top 5 for this database
        top5 = df.nsmallest(5, "adj_p_value")
        print(f"    Top 5 terms (by adj p-value):")
        for _, row in top5.iterrows():
            print(f"      [{row['adj_p_value']:.2e}] {row['term'][:70]}")
            print(f"               overlap={row['n_overlap']}  "
                  f"combined_score={row['combined_score']:.1f}")

# ── Combine and save ───────────────────────────────────────────────────────────
print(f"\n{'='*56}")
print("Saving results...")

if not all_results:
    print("ERROR: No enrichment results returned. Check internet connection.")
    sys.exit(1)

combined = pd.concat(all_results, ignore_index=True)

# Save full results
full_csv = PHASE2_OUT / "enrichment_results_full.csv"
combined.to_csv(full_csv, index=False)
print(f"  Full results: {full_csv.name}  ({len(combined)} terms)")

# Save significant results only (adj_p < 0.05), best gene list per term
sig = combined[combined["adj_p_value"] < 0.05].copy()
sig_csv = PHASE2_OUT / "enrichment_results_significant.csv"
sig.to_csv(sig_csv, index=False)
print(f"  Significant (adj_p<0.05): {sig_csv.name}  ({len(sig)} terms)")

# ── Summary table by database ──────────────────────────────────────────────────
print(f"\n{'='*56}")
print("PATHWAY ENRICHMENT SUMMARY")
print(f"{'='*56}")

for db in DATABASES:
    db_sig = sig[sig["database"] == db]
    if db_sig.empty:
        print(f"\n{db}: no significant terms")
        continue
    # Best results = top-100 gene list (most specific signal usually)
    db_top = (db_sig
              .sort_values("adj_p_value")
              .drop_duplicates("term")
              .head(15))
    print(f"\n{db} — top significant terms:")
    for _, row in db_top.iterrows():
        genes_str = row["overlap_genes"]
        if genes_str and len(genes_str) > 60:
            genes_str = genes_str[:60] + "..."
        print(f"  [{row['adj_p_value']:.2e}] {row['term'][:65]}")
        print(f"           overlap={row['n_overlap']}  "
              f"genes: {genes_str}")

print(f"\n{'='*56}")
print("Done. Paste full output into chat.")
