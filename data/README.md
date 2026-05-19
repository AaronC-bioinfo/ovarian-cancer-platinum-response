# Data

## Download Instructions

This project uses the **TCGA Ovarian Serous Cystadenocarcinoma (OV) — PanCancer Atlas 2018** dataset.

### Required files

Place all files in `data/raw/ov_tcga_pan_can_atlas_2018/`:

| File | Description |
|------|-------------|
| `data_clinical_patient.txt` | Patient clinical data (survival, stage, etc.) |
| `data_timeline_treatment.txt` | Treatment timeline (drug names, dates) |
| `data_mrna_seq_v2_rsem.txt` | mRNA expression matrix (RSEM-normalised) |

### Download from cBioPortal

1. Go to: https://www.cbioportal.org/study/summary?id=ov_tcga_pan_can_atlas_2018
2. Click **"Download"** → **"Compressed"**
3. Extract the archive into `data/raw/`
4. Rename the folder to `ov_tcga_pan_can_atlas_2018` if needed

Alternatively via the cBioPortal Data Hub:
```bash
curl -o data/raw/ov_tcga_pan_can_atlas_2018.tar.gz \
  "https://cbioportal-datahub.s3.amazonaws.com/ov_tcga_pan_can_atlas_2018.tar.gz"

tar -xzf data/raw/ov_tcga_pan_can_atlas_2018.tar.gz -C data/raw/
```

### Data overview

| Attribute | Value |
|-----------|-------|
| Cancer type | Ovarian Serous Cystadenocarcinoma |
| Patients | ~585 |
| mRNA features | ~20,500 genes |
| Expression type | RNA-seq V2 RSEM |
| Platform | Illumina HiSeq |

> **Note:** Raw data files are excluded from version control via `.gitignore`.
> The processed feature matrices are stored in `outputs/results/` for reproducibility.
