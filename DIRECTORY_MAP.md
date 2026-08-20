# Directory Map

Quick reference for how directories map to the analysis phases described in the
manuscript and `PROJECT_LOG.md`. Written 2026-07-20 (Phase 5 of the audit fixes).
Directories are intentionally **not** renamed, to avoid breaking hardcoded paths in
the R/Python scripts and in git history — this file documents the mapping instead.

## Analysis phase → directory

| Manuscript / log name | Scripts | Outputs |
|---|---|---|
| Core pipeline (Findings 1–3) | `src/`, `run.py`, `run_ablation_study.py` | `outputs/` |
| Phase 2 (Cox, RF/SHAP importance, enrichment) | `phase2/` | `phase2/outputs/` |
| External validation (Finding 3) | `validation/` | `validation/outputs/`, `data/external/` |
| **Enhancement 3 — tumour cellularity (ESTIMATE)** | `src/cellularity/` | `cellularity/` |
| **Enhancement 4 — HRD / BRCA** | `src/hrd/` | `hrd/` |
| **Enhancement 5 — expression-augmented Cox** | `enhancement5/` | `enhancement5/outputs/` |
| Multi-cancer replication (LUAD, COADREAD) | `multi_cancer/` | `multi_cancer/outputs/` |
| Figures | `figures/` (canonical) | `outputs/figures/`, `figures/` |
| Audit + fix artifacts (2026-07-20) | `fixes/` | `fixes/`, `AUDIT_2026-07-20.md` |
| Archived / superseded | `archive/` | — |

So when the manuscript says "Enhancement 4 (HRD/BRCA)", the code is in `src/hrd/`
and the results are in `hrd/`. Likewise Enhancement 3 ↔ `cellularity/`.

## Duplicate files — canonical copy

Both copies in each pair are byte-identical. The canonical copy is the one to edit;
the other is a leftover and can be removed by a human (not deleted here per the
no-delete guardrail).

| File | Canonical | Duplicate (leftover) | Why |
|---|---|---|---|
| `figure1_pipeline.py` | `figures/figure1_pipeline.py` | `./figure1_pipeline.py` | `figures/` copy is newer and sits with the rendered PNGs |
| `figure2_ablation.py` | `figures/figure2_ablation.py` | `./figure2_ablation.py` | same |
| `figure3_validation.py` | `figures/figure3_validation.py` | `./figure3_validation.py` | same |
| `03_pathway_enrichment_corrected.py` | `src/cellularity/03_pathway_enrichment_corrected.py` | `src/03_pathway_enrichment_corrected.py` | cellularity copy is newer and sits with the other Enhancement 3 scripts |

## New files added by the 2026-07-20 fix pass

- `fixes/phase1_rerun_clean_auc.py` — canonical clean-AUC re-run (Phase 1).
- `fixes/phase1_provenance.md` — investigation of the stale AUC table.
- `fixes/phase4_corrected_values.csv` — FLNA range, permutation range, ribosome
  significance by size, Enh5 per-fold α distribution.
- `outputs/results/clean_auc_table.csv` (+ `_raw.csv`) — locked LR row; RF/SVM pending.
- `validation/outputs/combat_diagnostics.csv` — written when `05_batch_correction.R` re-runs.
- `phase2/outputs/cox_summary_stats.csv` — written when `phase2_02_cox_model.R` re-runs.
- `hrd/brca_cox_summary.csv` — written when `src/hrd/02_cox_model_with_brca.R` re-runs.
- `enhancement5/outputs/final_model_alpha.csv` — written when `enhancement5_expression_cox.R` re-runs.
