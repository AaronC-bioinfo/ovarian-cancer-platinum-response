# download_multi_cancer.ps1
# Downloads BRCA, LUAD, COAD PanCancer Atlas 2018 datasets from cBioPortal
# Run from project root:
#   .\multi_cancer\download_multi_cancer.ps1

$BASE_URL = "https://cbioportal-datahub.s3.amazonaws.com"
$OUT_DIR  = "D:\ALIENWARE\WORK DATA\George Mason\Course Work\3rd Sem FALL 2025\BINF 760 ML\Project data"

$studies = @(
    @{ id = "brca_tcga_pan_can_atlas_2018"; label = "BRCA" },
    @{ id = "luad_tcga_pan_can_atlas_2018"; label = "LUAD" },
    @{ id = "coad_tcga_pan_can_atlas_2018"; label = "COAD" }
)

foreach ($study in $studies) {
    $id    = $study.id
    $label = $study.label
    $url   = "$BASE_URL/$id.tar.gz"
    $dest  = Join-Path $OUT_DIR "$id.tar.gz"
    $unzip = Join-Path $OUT_DIR $id

    Write-Host ""
    Write-Host "========================================"
    Write-Host "Downloading $label ($id)"
    Write-Host "URL : $url"
    Write-Host "Dest: $dest"
    Write-Host "========================================"

    if (Test-Path $unzip) {
        Write-Host "  Directory already exists — skipping download: $unzip"
        continue
    }

    # Download
    try {
        $start = Get-Date
        Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
        $elapsed = ((Get-Date) - $start).TotalSeconds
        $size = (Get-Item $dest).Length / 1MB
        Write-Host "  Downloaded: $([math]::Round($size,1)) MB in $([math]::Round($elapsed,1))s"
    } catch {
        Write-Host "  ERROR downloading $label : $_"
        Write-Host "  Trying alternate URL format..."
        # Alternate: some studies use .zip
        $url2  = "$BASE_URL/$id.zip"
        $dest2 = Join-Path $OUT_DIR "$id.zip"
        try {
            Invoke-WebRequest -Uri $url2 -OutFile $dest2 -UseBasicParsing
            Write-Host "  Downloaded via .zip"
            $dest = $dest2
        } catch {
            Write-Host "  ERROR: both .tar.gz and .zip failed for $label"
            Write-Host "  Manual download URL: https://www.cbioportal.org/study/summary?id=$id"
            continue
        }
    }

    # Extract
    Write-Host "  Extracting to $unzip ..."
    try {
        # tar is available natively in Windows 10/11
        $null = New-Item -ItemType Directory -Force -Path $unzip
        tar -xzf $dest -C $unzip --strip-components=1
        Write-Host "  Extraction complete."
        # Remove archive to save space
        Remove-Item $dest -Force
        Write-Host "  Archive removed."
    } catch {
        Write-Host "  ERROR extracting: $_"
        Write-Host "  Archive left at: $dest"
        Write-Host "  Extract manually with: tar -xzf `"$dest`" -C `"$unzip`""
    }

    # Verify key file exists
    $rsem = Join-Path $unzip "data_mrna_seq_v2_rsem.txt"
    if (Test-Path $rsem) {
        $lines = (Get-Content $rsem | Measure-Object -Line).Lines
        Write-Host "  VERIFIED: data_mrna_seq_v2_rsem.txt found ($lines lines)"
    } else {
        Write-Host "  WARNING: data_mrna_seq_v2_rsem.txt not found in $unzip"
        Write-Host "  Files present:"
        Get-ChildItem $unzip -Name | ForEach-Object { Write-Host "    $_" }
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "All downloads complete."
Write-Host "Data directory: $OUT_DIR"
Write-Host ""
Write-Host "Expected directories:"
foreach ($study in $studies) {
    $path = Join-Path $OUT_DIR $study.id
    $exists = if (Test-Path $path) { "EXISTS" } else { "MISSING" }
    Write-Host "  [$exists] $path"
}
Write-Host "========================================"
