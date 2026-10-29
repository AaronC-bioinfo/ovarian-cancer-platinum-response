# A7 — Leakage ablation rerun in the pinned environment (pre-run note)

Written 2026-10-29 ~18:20 ET, **before** the rerun. Do not edit after the run; add results under "Post-run" at the bottom.

## Why
The independent audit (`audit_v3/AUDIT_REPORT_v3.md`, blocker B1) found that the leakage result in v3 (abstract, Results "Feature-selection leakage…", Fig 4) comes from `outputs/results/ablation_*` files dated 2026-06-18. No record shows which scikit-learn version produced them, and RF/SVM output in this pipeline changes between scikit-learn versions (`label_validity/outputs/04a_rf_determinism*.txt`). Aaron chose option (a) on 2026-10-29: rerun the existing ablation **unchanged** on the host in the pinned environment, regenerate Fig 4, and describe the ablation's own preprocessing in the Methods.

## What is run (no code changes)
- Script: `run_ablation_study.py` (unchanged), with `src/ablation.py` and `src/preprocessing.py` (unchanged).
- Its preprocessing, as the code stands (stated here so the Methods can describe it):
  - raw RSEM values from `clean_expression()`: no log transform, all genes in the file
  - platinum-treated patients by exact CARBOPLATIN/CISPLATIN match
  - OS thresholds 12/18/24 months
  - 30 stratified 80/20 splits per condition (seeds = base seed + repeat)
  - top 500 genes by variance (unsupervised) or by F-score (supervised), computed on the full data ("leaky") vs on the training split only ("correct")
  - StandardScaler fitted on the training split; LR/RF/SVM from config
- Config: `config/config_ablation_pinned_2026-10-29.yaml`, a copy of `config/config.yaml` with three lines changed:
  - `data_dir` → `C:/PROJECTS/OV Data/Project data/ov_tcga_pan_can_atlas_2018`. This is the same path A4–A6 used. The June run used a `D:/ALIENWARE/...` copy, which is not reachable from here, so whether the two files are identical is not checked.
  - `results_dir` → `outputs/results_pinned_2026-10-29`
  - `figures_dir` → `outputs/figures_pinned_2026-10-29`

  The June files in `outputs/results/` are therefore **not overwritten**.
- The script also runs the split-variance ablation. Its outputs are written but **not used** (rule: never use `ablation_split_variance_summary.csv`).

## Predictions (June values for reference: supervised mean at 18/24 mo +0.207; unsupervised +0.003)
- **P1** — Logistic-regression rows reproduce the June summaries within ±0.01 AUC, for each row in both ablations. LR is expected to be the least version-sensitive. If P1 fails, the data file or preprocessing differs from June: **stop and diagnose before using any pinned values.**
- **P2** — Supervised mean inflation at 18/24 months (3 models × 2 thresholds) is between +0.15 and +0.27.
- **P3** — Unsupervised mean inflation at 18/24 months is between −0.02 and +0.02.
- **P4** — At 18 and 24 months, supervised inflation exceeds unsupervised inflation for every model (6/6).

## Decision rule
- If P1 holds, v3 reports the pinned values (abstract, Results, Fig 4, S7 Table) **whatever they are**, including if P2–P4 fail. The June values are recorded as superseded in this file, not deleted.
- The Methods will describe this analysis's own preprocessing (raw RSEM, all genes) and say that it differs from the classifier pipeline used in A4–A6.
- `figures/v3/make_figures_v3.py` will read F4 inputs from `outputs/results_pinned_2026-10-29/`.

## Commands (Aaron, PowerShell, from the repo root)
```powershell
cd C:\PROJECTS\ovarian-cancer-platinum-response
$PY = "C:\Users\AMAC_WORK\AppData\Local\Python\pythoncore-3.14-64\python.exe"
New-Item -ItemType Directory -Force outputs\results_pinned_2026-10-29 | Out-Null
& $PY -c "import sys,sklearn,numpy,pandas,scipy; print(sys.version); print('sklearn',sklearn.__version__,'numpy',numpy.__version__,'pandas',pandas.__version__,'scipy',scipy.__version__)" | Out-File -Encoding utf8 outputs\results_pinned_2026-10-29\ENVIRONMENT.txt
Get-Content outputs\results_pinned_2026-10-29\ENVIRONMENT.txt
& $PY run_ablation_study.py --config config\config_ablation_pinned_2026-10-29.yaml --n-repeats 30 2>&1 | Out-File -Encoding utf8 outputs\results_pinned_2026-10-29\run_log.txt
Get-Content outputs\results_pinned_2026-10-29\run_log.txt -Tail 15
```

## Deviation 1 (2026-10-29 ~18:22 ET, before the full rerun)
- First host run (18:15) completed the unsupervised ablation, then crashed in the supervised ablation. scikit-learn 1.9.0 (via narwhals) rejects DataFrames with duplicate column names. The RSEM file has duplicate gene symbols, including 13 blank symbols read as "nan". `f_classif` received such a DataFrame. Log: `outputs/results_pinned_2026-10-29/run_log.txt` (copied to `run_log_attempt1_crashed.txt`; its CSVs to `attempt1_crashed/`).
- Change, approved by Aaron 18:19 ET: `src/ablation.py` l.62 `f_classif(X_filled, y)` → `f_classif(X_filled.to_numpy(), y)`; l.233–234 (supervised loop only) `scaler.fit_transform(Xtr)` / `scaler.transform(Xte)` → `.to_numpy()` inputs. The arrays have the same column order, so the computation is unchanged.
- Equivalence check (VM, scikit-learn 1.7.2, scratch copies outside the repo): `run_supervised_leakage_ablation` at 18 months, 3 repeats, original vs patched → identical output (`DataFrame.equals` True; max |ΔAUC| 0).
- Observed in the same check: LR and SVM AUCs equal the June raw file for seeds 42–44, but RF differs. So the June run was not scikit-learn 1.7.2 either.
- First-run unsupervised results (seen before this change): LR rows identical to June (P1 holds for the unsupervised ablation); 18/24-month mean inflation +0.0056. The full rerun regenerates these deterministically.

## Post-run
Full rerun completed on the host at 2026-10-29 18:19–18:23 ET. Environment: `outputs/results_pinned_2026-10-29/ENVIRONMENT.txt`: Python 3.14.5, scikit-learn 1.9.0, numpy 2.4.6, pandas 3.0.3, scipy 1.17.1. Outputs: `outputs/results_pinned_2026-10-29/`. The unsupervised CSVs are identical to the first (crashed) attempt (`DataFrame.equals` True). Aligned cohorts: 214 / 206 / 199 patients at 12 / 18 / 24 months (11 / 22 / 36 non-responders); 20,531 genes.

| | 18/24-mo mean inflation, pinned | June (superseded) |
|---|---|---|
| Supervised F-score | +0.2080 (range +0.0645 to +0.3384) | +0.2072 (+0.0645 to +0.3384) |
| Unsupervised variance | +0.0056 (range −0.0397 to +0.0300) | +0.0033 |

Scorecard:
- **P1 — held.** Every LR row in both ablations is identical to June to 4 dp (12/18/24 months).
- **P2 — held.** Supervised mean +0.208, within +0.15 to +0.27.
- **P3 — held.** Unsupervised mean +0.006, within ±0.02.
- **P4 — held.** Supervised > unsupervised for 6/6 model × threshold rows at 18/24 months.

Differences from June are confined to random-forest rows (all thresholds, both ablations) and unsupervised SVM rows at 12 and 18 months. This is consistent with scikit-learn version sensitivity.

Per the decision rule, v3 now uses these pinned values. `figures/v3/make_figures_v3.py` reads F4 from `outputs/results_pinned_2026-10-29/` (the old F1–F4 and figure_values.md are copied to `figures/v3/superseded_june-ablation_2026-10-29/`). `ablation_split_variance_*` were written by the script and are not used.
