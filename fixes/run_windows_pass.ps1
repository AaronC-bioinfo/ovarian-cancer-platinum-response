<#
    run_windows_pass.ps1
    ?"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"??"?
    Consolidated re-run of every patched script from the 2026-07-20 fix pass,
    in the AUTHORS' environment (Windows, Python 3.14, R 4.6.0), so the
    RF/SVM AUCs and all R-derived numbers come from the real pipeline rather
    than the audit sandbox.

    Run from the project root:
        cd C:\PROJECTS\ovarian-cancer-platinum-response
        powershell -ExecutionPolicy Bypass -File fixes\run_windows_pass.ps1

    After it finishes, hand the four/five output CSVs back to the audit session:
        outputs/results/clean_auc_table.csv
        validation/outputs/combat_diagnostics.csv
        phase2/outputs/cox_summary_stats.csv
        hrd/brca_cox_summary.csv
        enhancement5/outputs/final_model_alpha.csv
#>

$ErrorActionPreference = "Stop"
$root   = "C:\PROJECTS\ovarian-cancer-platinum-response"
$py     = "C:\Users\AMAC_WORK\AppData\Local\Python\pythoncore-3.14-64\python.exe"
$rscript= "C:\Program Files\R\R-4.6.0\bin\Rscript.exe"
$tcga   = "D:\ALIENWARE\WORK DATA\George Mason\Course Work\3rd Sem FALL 2025\BINF 760 ML\Project data\ov_tcga_pan_can_atlas_2018"

Set-Location $root

Write-Host "=== 0. Sanity: interpreters + data ==="
& $py --version
& $rscript --version
if (-not (Test-Path $tcga)) { throw "TCGA data dir not found: $tcga" }
Write-Host "TCGA data dir OK`n"

Write-Host "=== 0b. Report scikit-learn version (PIN THIS in requirements.txt) ==="
& $py -c "import sklearn; print('scikit-learn', sklearn.__version__)"
Write-Host ""

Write-Host "=== 1. Phase 1 ??" canonical clean AUC re-run (RF/SVM in your env) ==="
# Clear any sandbox checkpoints so this is a fresh run in YOUR environment.
if (Test-Path "fixes\.phase1_ckpt") { Remove-Item -Recurse -Force "fixes\.phase1_ckpt" }
& $py "fixes\phase1_rerun_clean_auc.py" --data-dir $tcga
Write-Host ""

Write-Host "=== 2. Phase 2 ??" external-validation ComBat diagnostics ==="
& $rscript "validation\05_batch_correction.R"
Write-Host ""

Write-Host "=== 3. Phase 3a - Cox baseline (C-index, log-rank, regenerates KM plot) ==="
& $rscript "phase2\phase2_02_cox_model.R"
Write-Host ""

Write-Host "=== 3b. Phase 3b ??" BRCA Cox (matched-subset n) ==="
& $rscript "src\hrd\02_cox_model_with_brca.R"
Write-Host ""

Write-Host "=== 3c. Phase 3c ??" Enhancement 5 (final-model alpha) ==="
Write-Host "    (this one is the slowest - nested CV + final refit)"
& $rscript "enhancement5\enhancement5_expression_cox.R"
Write-Host ""

Write-Host "=== DONE. Collected output files: ==="
$outs = @(
  "outputs\results\clean_auc_table.csv",
  "validation\outputs\combat_diagnostics.csv",
  "phase2\outputs\cox_summary_stats.csv",
  "hrd\brca_cox_summary.csv",
  "enhancement5\outputs\final_model_alpha.csv"
)
foreach ($o in $outs) {
  if (Test-Path $o) { Write-Host "`n----- $o -----"; Get-Content $o }
  else { Write-Host "`n!!! MISSING: $o" }
}
Write-Host "`nAlso verify phase2\outputs\km_risk_groups.png is now a full-size image (not ~1.3 KB)."

