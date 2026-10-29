# PLATINUM_STATUS — primary label definition (verbatim)

Source: The Cancer Genome Atlas Research Network. Integrated genomic analyses of ovarian carcinoma. *Nature* 2011;474:609–615, doi:10.1038/nature10166. **Supplementary Information, Supplementary Methods S1 ("Biospecimen Collection and Clinical Data"), SI pages 2–3.** Local copy: `C:\PROJECTS\OV Data\Project data\Literature\Supplementary information.pdf`. Extracted with `pdftotext -layout` on 2026-10-29 (one page break between "Platinum" and "status" removed; no other change).

## Definitions

> "Chemotherapy treatment details were reviewed to identify drugs prescribed for adjuvant therapy. The date of last primary platinum treatment was also determined from the available chemotherapy details and included adjuvant therapy and consolidation treatment when given consecutively following adjuvant therapy. The platinum free interval was defined as the interval from the date of last primary platinum treatment to the date of progression, date of recurrence, or date of last known contact if the patient is alive and has not recurred. Platinum status was defined as resistant if the platinum free interval was less than six months and the patient had progressed or recurred. Platinum status was defined as sensitive if the platinum free interval is six months or greater, there was no evidence of progression or recurrence, and the follow‐up interval was at least six months from the date of last primary platinum treatment. Patients who have not progressed or recurred and been followed for less than six months from the date of last primary platinum treatment were excluded from analyses regarding platinum status."

Related field (same section, SI p. 2):

> "PRIMARYTHERAPYOUTCOMESUCCESS was defined as the response to treatment determined after primary surgery and subsequent adjuvant chemotherapy."

Table S1.2 (`TCGA-OV-Clinical-Table_S1.2.xlsx`, sheet `FootnotestoTable`) footnote on the interval:

> "*The PlatinumFreeInterval is negative if the patient had received treatment after the date of progression/recurrence or if the date of last platinum treatment is after the date of last follow-up."

## Notes (stated, not interpreted)

- "Tooearly" is not named in the text; the excluded group in the last sentence is the group the category label describes. "Missing" is not defined in Methods S1.
- The sensitive definition reads "there was no evidence of progression or recurrence" alongside a platinum free interval ≥ 6 months. Quoted as printed; not resolved here.
- Clinical data current as of August 25, 2010 (main text).

## Count check

| Source | Sensitive | Resistant | Tooearly | Missing |
|---|---|---|---|---|
| TCGA 2011 SI, Methods S1 clinical table ("Platinum status") | 197 | 90 | — | — |
| Table S1.2 `PlatinumStatus` column | 197 | 90 | 58 | 143 |
| cBioPortal `ov_tcga_pub` `PLATINUM_STATUS` (gate G2, all patients) | 197 | 90 | 58 | 143 |
| Li et al. 2022, Data Sheet 2 (TCGA "Platinum_status") | 197 | 90 | — | — |

The cBioPortal field used as `label_platinum` is the published TCGA 2011 label, unchanged. Li 2022 trained on exactly this label (n = 287).

Table S1.2 also carries TCGA's own `PlatinumFreeInterval (mos)`. Not used in A1: the sensitivity label (`label_pfiplat6`) is derived independently from TCGA-CDR and the pan-can treatment timeline.
