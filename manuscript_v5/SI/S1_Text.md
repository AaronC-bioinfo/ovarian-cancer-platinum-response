---
title: "S1 Text. Pre-specified predictions and decision rules for each analysis, with observed outcomes"
---

This file reproduces, verbatim, the header of each analysis script (written before the analysis was run, unless marked post hoc, descriptive or exploratory) and its full summary (results, and post-run notes and scorecards). Text added after a run is marked as such in the summaries; headers were not edited after running. Scripts A8–A10 were deposited in the public repository before they were run (commits d5bd844 and e98b3d9), and A15 and A16, added after an external review, in commit d349b2b. The leakage rerun (A7) has its own pre-run note, reproduced in full.

# Gate G1–G4: label coverage and sources

*Status:* pre-specified. *Script:* `label_validity/00_gate_pfi_coverage.py`. *Summary:* `label_validity/outputs/00_gate_summary.md`.

## Header (verbatim)

```text
label_validity/00_gate_pfi_coverage.py
──────────────────────────────────────
Q2 reorganisation, decision gate G1–G3
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §3).

Descriptive counts and cross-tabs only. No models, no p-values, no scipy.
Cohorts are rebuilt with the repo's own functions (src.data_loader,
src.preprocessing) — nothing re-implemented — and checked against the
documented sizes (fixes/phase1_provenance.md: 489 platinum; 214/206/199 with
11/22/36 events) before anything else is reported.

Inputs (read-only)
──────────────────
  <data-root>/TCGA-CDR-SupplementalTableS1.xlsx          sheet "TCGA-CDR"
  <data-root>/ov_tcga_pan_can_atlas_2018/                clinical, treatment, status, RSEM header
  <data-root>/ov_tcga_pub/ov_tcga_pub/data_clinical_patient.txt   (TCGA Nature 2011)
  phase2/outputs/cox_patients_with_risk.csv              (432 Cox cohort)

Outputs → label_validity/outputs/
  gate_patient_table.csv   one row per patient, every gate field + provenance
  gate_g1_coverage.csv
  gate_g2_platinum_sources.csv
  gate_g3_crosstabs.csv    long-form cross-tabs
  00_gate_summary.md       predictions vs observed, pass/fail per gate

Usage
─────
  python label_validity/00_gate_pfi_coverage.py
  python label_validity/00_gate_pfi_coverage.py --data-root "C:/PROJECTS/OV Data/Project data"

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before this script was run — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Disclosure: while inspecting column names before writing this header, the
following were already seen and are NOT predictions:
  * CDR OV: 587 patients; PFI non-null 587 (414 events / 173 censored);
    PFI.time non-null 582; treatment_outcome_first_course categories and
    counts across all 587 OV patients; 45 rows marked Redacted.
  * Category labels (no counts) of ov_tcga_pub PLATINUM_STATUS
    {Missing, Resistant, Sensitive, Tooearly}, PRIMARY_THERAPY_OUTCOME_SUCCESS,
    treatment REGIMEN_INDICATION and platinum AGENT strings.
  * outputs/results/label_investigation_coverage_timeline.csv: the "142"
    is ROWS of data_timeline_status.txt in the platinum cohort, not patients.
Nothing below about intersections, ov_tcga_pub counts, timeline coverage or
concordance had been looked at.

G1  PFI coverage (CDR PFI and PFI.time both non-null)
  P1.1  ≥ 460 of the 489 platinum patients have CDR PFI.
  P1.2  Each classification cohort (12/18/24m) has ≥ 190 patients with PFI.
  P1.3  ≥ 410 of the 432 Cox patients have PFI.
  RULE  PASS if every classification cohort has ≥ 120 patients with PFI.

G2  Platinum-specific sources
  P2.1  ov_tcga_pub PLATINUM_STATUS ∈ {Resistant, Sensitive} for ≥ 250
        patients overall and ≥ 150 in the 24m classification cohort.
  P2.2  ≥ 80 % of the 489 platinum patients have a first-line (REGIMEN_INDICATION
        == "Adjuvant") platinum row with a non-missing STOP_DATE.
  P2.3  Where both exist, PFI-from-last-first-line-platinum < 183 d agrees with
        PLATINUM_STATUS == Resistant in ≥ 80 % of patients.
  P2.4  Substring matching of platinum AGENT strings adds ≤ 20 patients to the
        489 exact-match platinum cohort.
  RULE  PASS if either source gives a usable platinum label (Resistant/Sensitive,
        or a determinate short/long PFI-from-platinum) for ≥ 150 patients in
        the 24m classification cohort.

G3  Response field vs PFI vs OS labels
  P3.1  Unique patients with PRIMARY_THERAPY_OUTCOME_SUCCESS in the pan-can
        timeline, within the 489 platinum cohort: 120–142.
  P3.2  Of PD patients with a determinate platinum label, ≥ 70 % are
        Resistant / short PFI-from-platinum.
  P3.3  Of CR patients with a determinate platinum label, ≥ 70 % are
        Sensitive / long PFI-from-platinum.
  P3.4  Where pan-can PTOS and CDR treatment_outcome_first_course both exist,
        category agreement ≥ 95 % (same TCGA clinical source).
  P3.5  OS-threshold labels (18m, 24m) flag < 50 % of Resistant patients as
        non-responders (sensitivity < 0.5).
  RULE  "High" concordance = P(Resistant or short | PD) ≥ 0.80 with ≥ 10 PD
        patients. If lower, report it as a property of the resource; do not
        pick the convenient field.

Fixed definitions (stated, not tuned)
  * 6 months = 183 days.
  * PFI-from-platinum (days) = CDR PFI.time − max STOP_DATE over platinum rows
    with REGIMEN_INDICATION == "Adjuvant". Both are days from diagnosis.
    short: PFI == 1 and value < 183; long: value ≥ 183;
    indeterminate: PFI == 0 and value < 183; negative values are counted
    separately ("event before end of first-line platinum") and also classed short.
  * CDR PFI.time is from diagnosis. It is reported only as a distribution and as
    descriptive cross-tabs at 6 and 12 months from diagnosis; no label is
    chosen from it here (that is A1's job).
```

## Summary: results and scorecard (verbatim)

# Gate G1–G3 summary — label_validity/00_gate_pfi_coverage.py

Cohort reproduction (repo functions): platinum=489; 12m n=214; 12m events=11; 18m n=206; 18m events=22; 24m n=199; 24m events=36 — all match fixes/phase1_provenance.md. Cox cohort 432 read from phase2/outputs.

## G1 — CDR PFI coverage

```
            cohort   n  in_cdr  has_cdr_pfi  pfi_events  redacted
platinum_exact_489 489     489          488         366        38
           cox_432 432     432          432         317        30
           cls_12m 214     214          214         183         7
           cls_18m 206     206          206         179         7
           cls_24m 199     199          199         174         7
```

- P1.1 ≥460/489 platinum with PFI → observed 488
- P1.2 each cls cohort ≥190 → observed cls_12m: 214/214, cls_18m: 206/206, cls_24m: 199/199
- P1.3 ≥410/432 Cox → observed 432
- **G1 PASS** (rule: every cls cohort ≥120 with PFI)

## G2 — platinum-specific sources

```
            cohort   n  pub_Resistant  pub_Sensitive  pub_Tooearly  pub_Missing  pub_absent  pub_determinate  has_firstline_platinum_row  has_firstline_stop_date  pfi_plat6_short  pfi_plat6_long  pfi_plat6_indeterminate  pfi_plat_negative  either_determinate
      all_patients 587             90            197            58          143          99              287                         467                      438              115             275                       47                 19                 404
platinum_exact_489 489             87            190            57           87          68              277                         466                      437              115             274                       47                 19                 394
           cox_432 432             74            169            55           78          56              243                         409                      384               98             243                       43                 18                 345
           cls_12m 214             40            103            11           53           7              143                         199                      185               52             132                        1                  4                 185
           cls_18m 206             39            100            10           51           6              139                         192                      178               51             126                        1                  4                 178
           cls_24m 199             39             95            10           50           5              134                         187                      173               51             121                        1                  4                 173
```

- P2.1 pub Resistant/Sensitive ≥250 overall, ≥150 in cls_24m → observed 287 overall, 134 in cls_24m
- P2.2 ≥80% of 489 with first-line platinum STOP_DATE → observed 437/489 = 0.894 [0.863, 0.918]
- P2.3 PFI-from-platinum vs pub status agreement ≥0.80 → observed 268/272 = 0.985 [0.963, 0.994]
- P2.4 substring match adds ≤20 to 489 → observed +1 patients (1 with RNA-seq); exact-match patients not found by substring: 0
- **G2 PASS** (rule: ≥150 determinate in cls_24m from either source; observed 173)

## G3 — response field vs platinum label vs OS labels (platinum cohort, n=489)

- P3.1 unique pan-can PTOS patients 120–142 → observed 142 (0 with conflicting values)
- P3.2 P(Resistant/short | PD) ≥0.70 → combined 1/5 = 0.200 [0.036, 0.624]; pub status only 1/3 = 0.333 [0.061, 0.792]; PFI-from-platinum only 2/5 = 0.400 [0.118, 0.769]
- P3.3 P(Sensitive/long | CR) ≥0.70 → combined 75/80 = 0.938 [0.862, 0.973]; pub status only 51/55 = 0.927 [0.827, 0.971]; PFI-from-platinum only 74/80 = 0.925 [0.846, 0.965]
- P3.4 pan-can PTOS vs CDR first-course outcome agreement ≥0.95 → observed 141/142 = 0.993 [0.961, 0.999]
- P3.5 OS18 sensitivity for Resistant <0.5 → observed 11/49 = 0.224 [0.130, 0.359]
- P3.5 OS24 sensitivity for Resistant <0.5 → observed 17/49 = 0.347 [0.229, 0.487]
- **G3 FAIL** (rule: P(Resistant/short | PD) ≥0.80 with ≥10 PD)

Full cross-tabs: gate_g3_crosstabs.csv. Per-patient provenance: gate_patient_table.csv.
Combined platinum label = ov_tcga_pub PLATINUM_STATUS where Resistant/Sensitive, else PFI-from-first-line-platinum short/long. Proportions with Wilson 95% CI.

# Gate, post hoc: response-field sources

*Status:* post hoc. *Script:* `label_validity/00b_gate_posthoc_response_sources.py`. *Summary:* `label_validity/outputs/00b_posthoc_summary.md`.

## Header (verbatim)

```text
label_validity/00b_gate_posthoc_response_sources.py
───────────────────────────────────────────────────
POST HOC — NOT PRE-REGISTERED. Written 2026-10-29 after 00_gate_pfi_coverage.py
had run and its output had been read.

Why: pre-registered G3 used the response field from the pan-can
data_timeline_status.txt (142 patients, 5 PD with a platinum label) and failed
on power, not on concordance. The cross-tabs showed the same field is
populated far more widely in two other copies of the TCGA clinical data:
  * ov_tcga_pub data_clinical_patient.txt  PRIMARY_THERAPY_OUTCOME_SUCCESS
  * TCGA-CDR treatment_outcome_first_course
This script quantifies coverage and agreement of the three copies and repeats
the G3 concordance with each. It does not replace the G3 verdict in
00_gate_summary.md; it is reported beside it.

Reads only label_validity/outputs/gate_patient_table.csv. No new inputs.
Output: label_validity/outputs/00b_posthoc_summary.md, 00b_posthoc_table.csv
```

## Summary: results and scorecard (verbatim)

# POST HOC — response-field sources (not pre-registered)

Reads gate_patient_table.csv only. Categories mapped to CR/PR/SD/PD.

## Coverage of the response field by source

```
            cohort   n  pancan_n  pancan_CR  pancan_PR  pancan_SD  pancan_PD  pub_n  pub_CR  pub_PR  pub_SD  pub_PD  cdr_n  cdr_CR  cdr_PR  cdr_SD  cdr_PD  any_n
platinum_exact_489 489       142        116          8         11          7    366     257      53      22      34    424     300      59      26      39    425
           cls_12m 214        52         43          3          5          1    184     125      30      12      17    191     131      30      12      18    191
           cls_18m 206        45         38          3          4          0    179     122      30      11      16    184     126      30      11      17    184
           cls_24m 199        40         35          1          4          0    175     120      28      11      16    179     123      28      11      17    179
           cox_432 432       133        108          7         11          7    327     231      43      20      33    378     269      47      24      38    379
```

## Agreement between copies (platinum cohort, patients with both)

- pancan vs pub: 108/109 = 0.991 [0.950, 0.998]
- pancan vs cdr: 141/142 = 0.993 [0.961, 0.999]
- pub vs cdr: 365/365 = 1.000 [0.990, 1.000]

## G3 concordance repeated with each response source (platinum cohort)

### pancan
- P(Resistant | PD), pub status: 1/3 = 0.333 [0.061, 0.792]
- P(short | PD), PFI-from-platinum: 2/5 = 0.400 [0.118, 0.769]
- P(Sensitive | CR), pub status: 51/55 = 0.927 [0.827, 0.971]
- P(long | CR), PFI-from-platinum: 74/80 = 0.925 [0.846, 0.965]
- P(Resistant | PD or SD), pub status: 3/8 = 0.375 [0.137, 0.694]

Cross-tab vs pub PLATINUM_STATUS:
```
pub_platinum_status  Missing  Resistant  Sensitive  Tooearly  absent
resp_pancan                                                         
CR                         9          4         51        25      27
NA                        70         80        130        30      37
PD                         3          1          2         0       1
PR                         1          0          4         0       3
SD                         4          2          3         2       0
```
Cross-tab vs PFI-from-first-line-platinum:
```
pfi_plat6_class  NA  indeterminate  long  short
resp_pancan                                    
CR                8             28    74      6
NA               44             12   187    104
PD                0              2     3      2
PR                1              1     6      0
SD                0              4     4      3
```

### pub
- P(Resistant | PD), pub status: 15/18 = 0.833 [0.608, 0.942]
- P(short | PD), PFI-from-platinum: 16/27 = 0.593 [0.407, 0.755]
- P(Sensitive | CR), pub status: 156/191 = 0.817 [0.756, 0.865]
- P(long | CR), PFI-from-platinum: 181/220 = 0.823 [0.767, 0.868]
- P(Resistant | PD or SD), pub status: 20/28 = 0.714 [0.529, 0.847]

Cross-tab vs pub PLATINUM_STATUS:
```
pub_platinum_status  Missing  Resistant  Sensitive  Tooearly  absent
resp_pub                                                            
CR                        23         35        156        43       0
NA                        21          9         13        12      68
PD                        16         15          3         0       0
PR                        17         23         13         0       0
SD                        10          5          5         2       0
```
Cross-tab vs PFI-from-first-line-platinum:
```
pfi_plat6_class  NA  indeterminate  long  short
resp_pub                                       
CR               13             24   181     39
NA               28             16    53     26
PD                5              2    11     16
PR                5              1    20     27
SD                2              4     9      7
```

### cdr
- P(Resistant | PD), pub status: 15/18 = 0.833 [0.608, 0.942]
- P(short | PD), PFI-from-platinum: 18/30 = 0.600 [0.423, 0.754]
- P(Sensitive | CR), pub status: 156/191 = 0.817 [0.756, 0.865]
- P(long | CR), PFI-from-platinum: 205/251 = 0.817 [0.764, 0.860]
- P(Resistant | PD or SD), pub status: 20/28 = 0.714 [0.529, 0.847]

Cross-tab vs pub PLATINUM_STATUS:
```
pub_platinum_status  Missing  Resistant  Sensitive  Tooearly  absent
resp_cdr                                                            
CR                        24         35        156        45      40
NA                        20          9         14        10      12
PD                        16         15          3         0       5
PR                        17         23         12         0       7
SD                        10          5          5         2       4
```
Cross-tab vs PFI-from-first-line-platinum:
```
pfi_plat6_class  NA  indeterminate  long  short
resp_cdr                                       
CR               21             28   205     46
NA               16             12    23     14
PD                7              2    12     18
PR                6              1    24     28
SD                3              4    10      9
```

## CDR-PD patients with PFI-from-platinum ≥183 d (n=12)

```
             pub_platinum_status  cdr_PFI  cdr_PFI_time_d  firstline_platinum_stop_d  pfi_from_platinum_d
PATIENT_ID                                                                                               
TCGA-04-1342             Missing      1.0           563.0                      142.0                421.0
TCGA-04-1343             Missing      1.0           361.0                      170.0                191.0
TCGA-09-0367             Missing      1.0           547.0                       92.0                455.0
TCGA-09-2054             Missing      1.0           637.0                      161.0                476.0
TCGA-23-1123             Missing      1.0          1018.0                      250.0                768.0
TCGA-23-2081             Missing      1.0          2342.0                      173.0               2169.0
TCGA-25-1320           Sensitive      1.0           424.0                      181.0                243.0
TCGA-25-2042             Missing      1.0           396.0                      123.0                273.0
TCGA-29-1766           Sensitive      1.0           672.0                      189.0                483.0
TCGA-57-1582             Missing      1.0           731.0                      170.0                561.0
TCGA-61-2002             Missing      0.0           547.0                      129.0                418.0
TCGA-61-2096                 NaN      1.0           421.0                       79.0                342.0
```

# A1: label construction

*Status:* pre-specified. *Script:* `label_validity/01_labels_master.py`. *Summary:* `label_validity/outputs/01_labels_summary.md`.

## Header (verbatim)

```text
label_validity/01_labels_master.py
──────────────────────────────────
Q2 analysis A1 — label construction
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4; label decision 2026-10-29).

One tidy table, one row per platinum-treated patient (exact-match cohort, n=489),
every label with its provenance. Downstream scripts (A2–A5) read only this file.

Input:  label_validity/outputs/gate_patient_table.csv
        (built by 00_gate_pfi_coverage.py from the raw sources: TCGA-CDR
        Supplemental Table S1, cBioPortal ov_tcga_pub and
        ov_tcga_pan_can_atlas_2018; OS-threshold cohorts rebuilt with
        src.preprocessing and checked against fixes/phase1_provenance.md)
Output: label_validity/outputs/labels_master.csv
        label_validity/outputs/01_labels_summary.md

Labels (1 = non-responder / resistant, 0 = responder / sensitive, NA = undetermined)
──────────────────────────────────────────────────────────────────────────────────
  label_platinum   PRIMARY (Aaron, 2026-10-29). ov_tcga_pub PLATINUM_STATUS:
                   Resistant → 1, Sensitive → 0; Tooearly, Missing, absent → NA.
                   The TCGA 2011 wording of this definition is NOT yet quoted
                   verbatim (open item); the field is used as published.
  label_pfiplat6   SENSITIVITY. PFI from end of first-line platinum =
                   CDR PFI.time − max STOP_DATE of platinum rows with
                   REGIMEN_INDICATION == "Adjuvant" (both days from diagnosis).
                   short (PFI==1 and < 183 d, incl. negative) → 1; ≥ 183 d → 0;
                   PFI==0 and < 183 d → NA.
  label_response   PD or SD → 1; CR or PR → 0, from the first-course response
                   field. Source order fixed in advance: CDR
                   treatment_outcome_first_course, else ov_tcga_pub
                   PRIMARY_THERAPY_OUTCOME_SUCCESS, else pan-can
                   data_timeline_status.txt. (The three copies agree: pub vs CDR
                   365/365, pan-can vs CDR 141/142 — 00b_posthoc_summary.md.)
  label_os12/18/24 Existing OS-threshold labels exactly as in the v2 paper
                   (src.preprocessing.assign_response_label), defined only
                   inside the OS cohorts. 12m is supplement-only.
  pfi_time_d, pfi_event        CDR PFI.time (days from diagnosis), CDR PFI.
  pfi_from_platinum_d          as above, continuous.

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS / CHECKS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
A1 is a construction step. Its counts inside the OS cohorts were already
observed in the gate, so they are ASSERTIONS (the script stops if any fails),
not predictions:
  C1  cls_24m: label_platinum 39 resistant / 95 sensitive.
  C2  cls_24m: label_pfiplat6 51 short / 121 long.
  C3  cls_24m: label_response determinate = 179.
  C4  label_os18/os24 event counts 22 / 36 inside their cohorts.
  C5  pan-can-only response values used as fallback: ≤ 1 patient.
New (not yet seen) — predictions:
  P1  platinum ∩ RNA-seq has 150–200 patients with a determinate label_platinum
      (more than the 134 in cls_24m, because the OS cohorts drop patients
      censored before the threshold).
  P2  In platinum ∩ RNA-seq, resistant prevalence of label_platinum is 0.25–0.35.
```

## Summary: results and scorecard (verbatim)

# A1 — labels_master.csv summary

All construction checks C1–C5 passed (script stops otherwise).

Counts per label (rows: `<label>_1` = non-responder/resistant, `_0` = responder/sensitive):

```
cohort            platinum_489  platinum_rnaseq  cls_12m  cls_18m  cls_24m  cox_432
n                          489              251      214      206      199      431
label_platinum_1            87               41       40       39       39       74
label_platinum_0           190              104      103      100       95      168
label_pfiplat6_1           115               53       52       51       51       98
label_pfiplat6_0           274              135      132      126      121      242
label_response_1            65               35       30       28       28       62
label_response_0           360              184      161      156      151      316
label_os12_1                11               11       11       11       11       10
label_os12_0               203              203      203      195      188      188
label_os18_1                22               22       22       22       22       21
label_os18_0               184              184      184      184      177      170
label_os24_1                36               36       36       36       36       34
label_os24_0               163              163      163      163      163      150
```

- P1 platinum ∩ RNA-seq with determinate label_platinum: 145 (predicted 150–200); platinum ∩ RNA-seq n = 251
- P2 resistant prevalence in that set: 0.283 (predicted 0.25–0.35)
- label_response source: {'cdr': 424, <NA>: 64, 'ov_tcga_pub': 1}
- PLATINUM_STATUS raw values (platinum ∩ RNA-seq): {'Sensitive': 104, 'Missing': 61, 'Resistant': 41, 'Tooearly': 36, 'absent': 9}

Open item: TCGA 2011 wording of PLATINUM_STATUS not yet quoted verbatim.

# A2: agreement (RNA-seq OS labels)

*Status:* pre-specified. *Script:* `label_validity/02_label_agreement.py`. *Summary:* `label_validity/outputs/02_agreement_summary.md`.

## Header (verbatim)

```text
label_validity/02_label_agreement.py
────────────────────────────────────
Q2 analysis A2 — how the response labels relate to each other
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A2).

Reads only label_validity/outputs/labels_master.csv (A1).

Analyses (fixed before running)
  1. Every pair of labels among: label_platinum (primary), label_pfiplat6,
     label_response, label_os18, label_os24. label_os12 pairs go to the
     supplement table only. Population: platinum-treated patients with both
     labels determinate (OS labels exist only inside their OS cohorts, so any
     pair with an OS label is automatically within platinum ∩ RNA-seq).
     Output per pair: 2×2 table, n, raw agreement, Cohen's κ with 95% CI
     (2,000-resample percentile bootstrap, seed 42, resampling patients).
  2. OS-threshold labels as "tests" against each platinum/response label as
     reference: sensitivity = P(OS label = 1 | reference = 1),
     specificity = P(OS label = 0 | reference = 0), Wilson 95% CIs.
  Repeated restricted to platinum ∩ RNA-seq as a sensitivity check (only pairs
  without an OS label change).
  Descriptive estimates with CIs only; no hypothesis tests, so no multiplicity
  correction applies to A2.

Outputs → label_validity/outputs/
  a2_pairwise_agreement.csv, a2_os_sens_spec.csv, 02_agreement_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already seen (disclosed, so partly not predictions): gate G3 gave OS18 and OS24
sensitivity of 11/49 and 17/49 against the COMBINED platinum label (pub status,
else PFI-from-platinum); gate G2 gave pub status vs PFI-from-platinum raw
agreement 268/272; post hoc 00b gave P(Resistant | PD) 15/18 and
P(Sensitive | CR) 156/191. No κ has been computed; the pure label_platinum
sensitivities have not been computed.

  P1  κ(OS18, platinum) < 0.40 and κ(OS24, platinum) < 0.40.
  P2  κ(OS18, pfiplat6) < 0.40 and κ(OS24, pfiplat6) < 0.40.
  P3  Sensitivity of OS18 and of OS24 for label_platinum = 1 is < 0.50.
  P4  Specificity of OS18 and OS24 for label_platinum = 0 is > 0.85.
  P5  κ(platinum, pfiplat6) ≥ 0.80 (check; agreement already seen).
  P6  κ(platinum, response) between 0.30 and 0.60.

DECISION RULE (for the paper's claim "OS-threshold labels do not measure
platinum response in TCGA-OV"):
  Supported if κ(OS18, platinum) and κ(OS24, platinum) both have point
  estimate < 0.40 AND upper 95% bound < 0.60.
  Not supported if either point estimate ≥ 0.60.
  Otherwise: "partial agreement", reported as such.
```

## Summary: results and scorecard (verbatim)

# A2 — label agreement

Population: platinum-treated patients with both labels determinate. κ 95% CI: 2,000-resample bootstrap (seed 42).
Coding: 1 = non-responder / resistant. Cells a1b1 … a0b0 are label_a × label_b.

```
       label_a        label_b   n  a1b1  a1b0  a0b1  a0b0  agreement  kappa  kappa_lo  kappa_hi
label_platinum label_pfiplat6 272    85     0     4   183      0.985  0.966     0.930     0.992
label_platinum label_response 255    20    58     8   169      0.741  0.257     0.137     0.380
label_platinum     label_os18 139     5    34     2    98      0.741  0.144     0.014     0.293
label_platinum     label_os24 134    11    28     7    88      0.739  0.248     0.073     0.416
label_pfiplat6 label_response 353    27    74    22   230      0.728  0.213     0.100     0.322
label_pfiplat6     label_os18 177    11    40     5   121      0.746  0.221     0.081     0.366
label_pfiplat6     label_os24 172    18    33    10   111      0.750  0.311     0.154     0.463
label_response     label_os18 184     7    21     8   148      0.842  0.245     0.060     0.440
label_response     label_os24 179    10    18    17   134      0.804  0.248     0.067     0.430
    label_os18     label_os24 199    22     0    14   163      0.930  0.720     0.567     0.848
```

## Predictions vs observed

- P1 κ(OS18, platinum) κ = 0.144 [0.014, 0.293], n = 139, agreement 0.741; κ(OS24, platinum) κ = 0.248 [0.073, 0.416], n = 134, agreement 0.739 — predicted both < 0.40
- P2 κ(OS18, pfiplat6) κ = 0.221 [0.081, 0.366], n = 177, agreement 0.746; κ(OS24, pfiplat6) κ = 0.311 [0.154, 0.463], n = 172, agreement 0.750 — predicted both < 0.40
- P3 sensitivity for platinum-resistant: OS18 5/39 = 0.128 [0.056, 0.267]; OS24 11/39 = 0.282 [0.165, 0.438] — predicted < 0.50
- P4 specificity for platinum-sensitive: OS18 98/100 = 0.980 [0.930, 0.994]; OS24 88/95 = 0.926 [0.856, 0.964] — predicted > 0.85
- P5 κ(platinum, pfiplat6) κ = 0.966 [0.930, 0.992], n = 272, agreement 0.985 — predicted ≥ 0.80
- P6 κ(platinum, response) κ = 0.257 [0.137, 0.380], n = 255, agreement 0.741 — predicted 0.30–0.60

**Decision rule: SUPPORTED** (OS-threshold labels vs the primary platinum label).

## OS labels as tests against each reference (sensitivity / specificity, Wilson 95% CI)

```
     reference   os_label   n  ref_pos  tp  sensitivity  sens_lo  sens_hi  ref_neg  tn  specificity  spec_lo  spec_hi
label_platinum label_os12 143       40   1        0.025    0.004    0.129      103 103        1.000    0.964    1.000
label_platinum label_os18 139       39   5        0.128    0.056    0.267      100  98        0.980    0.930    0.994
label_platinum label_os24 134       39  11        0.282    0.165    0.438       95  88        0.926    0.856    0.964
label_pfiplat6 label_os12 184       52   6        0.115    0.054    0.230      132 132        1.000    0.972    1.000
label_pfiplat6 label_os18 177       51  11        0.216    0.125    0.346      126 121        0.960    0.910    0.983
label_pfiplat6 label_os24 172       51  18        0.353    0.236    0.490      121 111        0.917    0.855    0.954
label_response label_os12 191       30   4        0.133    0.053    0.297      161 160        0.994    0.966    0.999
label_response label_os18 184       28   7        0.250    0.127    0.434      156 148        0.949    0.902    0.974
label_response label_os24 179       28  10        0.357    0.207    0.542      151 134        0.887    0.827    0.929
```

## Sensitivity check: platinum ∩ RNA-seq (pairs without OS labels)

```
       label_a        label_b   n  agreement  kappa  kappa_lo  kappa_hi
label_platinum label_pfiplat6 144      0.986  0.966     0.912     1.000
label_platinum label_response 136      0.772  0.300     0.122     0.470
label_pfiplat6 label_response 175      0.726  0.190     0.036     0.357
```

Supplement (12m): see rows with supplement = True in a2_pairwise_agreement.csv and a2_os_sens_spec.csv.

# A3: associations with BRCA1/2 and clinical characteristics (somatic BRCA1/2; RNA-seq OS labels)

*Status:* pre-specified. *Script:* `label_validity/03_known_groups.py`. *Summary:* `label_validity/outputs/03_known_groups_summary.md`.

## Header (verbatim)

```text
label_validity/03_known_groups.py
─────────────────────────────────
Q2 analysis A3, part 1 — known-groups validity of each response label
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A3).

Question: does each label separate patients along characteristics that a
platinum-response label should track (somatic BRCA1/2), and along ones an
overall-survival label might track instead (age, stage, residual disease)?

Population: platinum-treated patients (A1 cohort: exact carboplatin/cisplatin
match, n = 489) with the label determinate and the covariate non-missing.
The Cox part (03b_pfi_cox.R) keeps the v2 Cox cohort instead (phase2
definition, n = 432 / BRCA subset 335); the one-patient difference
(TCGA-29-1711, oxaliplatin only) is stated in both scripts.

Inputs
  label_validity/outputs/labels_master.csv           (A1)
  hrd/brca_status.csv                                 BRCA_any_mutated (somatic, non-silent; v2 Enhancement 4)
  <data-root>/ov_tcga_pan_can_atlas_2018/data_clinical_sample.txt   ANEUPLOIDY_SCORE, TMB_NONSYNONYMOUS (first sample per patient, as phase2)
  <data-root>/TCGA-CDR-SupplementalTableS1.xlsx       age_at_initial_pathologic_diagnosis, clinical_stage
  <data-root>/ov_tcga_pub/ov_tcga_pub/data_clinical_sample.txt     TUMOR_RESIDUAL_DISEASE (TCGA 2011)

Labels (1 = non-responder / resistant): label_platinum (primary), label_pfiplat6,
label_response, label_os18, label_os24; label_os12 in the supplement.

Tests (fixed before running)
  BRCA_any_mutated (1 vs 0)            Fisher exact; conditional OR of being label = 1 if mutant, 95% CI
  Stage IV vs I–III (CDR clinical_stage) Fisher exact; OR of label = 1 if stage IV
  Suboptimal residual (11–20 mm, >20 mm) vs optimal (no macroscopic, 1–10 mm)
                                        Fisher exact; OR of label = 1 if suboptimal
                                        (optimal ≤ 1 cm as defined in TCGA 2011 SI Methods S1)
  Aneuploidy score, TMB, age           Mann–Whitney U, two-sided; rank-biserial r
                                        (r > 0 = higher in label = 1)
  Multiplicity: Benjamini–Hochberg across the 6 tests within each label (one
  family per label). Raw p and BH q both reported.

Outputs → label_validity/outputs/a3_known_groups.csv, 03_known_groups_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already known (not predictions): TCGA 2011 SI Methods S1 reports that platinum
status was associated with residual disease among optimally debulked patients
and that microscopic residual disease was "independently associated with
platinum status (P = 0.005)". v2: BRCA HR 0.455 for OS (n = 335); aneuploidy
HR 1.021 for OS.

  P1  BRCA: OR < 1 (mutant → sensitive/responder) for label_platinum and
      label_pfiplat6, with the 95% CI excluding 1 for label_platinum.
  P2  BRCA: for label_os18 and label_os24 the OR is closer to 1 than for
      label_platinum, and the CI includes 1.
  P3  Residual: OR > 1 (suboptimal → resistant) for label_platinum, CI excluding 1.
  P4  Age: |r| ≥ 0.15 with older age → non-responder for label_os24; |r| < 0.15
      for label_platinum.
  P5  Aneuploidy and TMB: no BH-significant association (q ≥ 0.05) for any label.
  P6  Stage IV: OR > 1 for all labels; CI may include 1.

DECISION RULE (known-groups validity of each label, pre-specified):
  "BRCA-valid"   if OR(BRCA) < 1 and its 95% CI excludes 1;
  "direction only" if OR(BRCA) < 1 and the CI includes 1;
  "not supported" if OR(BRCA) ≥ 1.
```

## Summary: results and scorecard (verbatim)

# A3 part 1 — known-groups validity

Platinum-treated patients (A1 cohort) with label and covariate non-missing. OR = odds of label = 1 (non-responder/resistant) when the covariate = 1. r > 0 = higher values in label = 1. BH within each label (6 tests).

```
         label       covariate   n  n_label1          effect  estimate  ci_lo  ci_hi     p  q_bh_within_label
label_platinum        brca_mut 191        59              OR     0.000  0.000  0.535 0.003              0.020
label_platinum        stage_iv 277        87              OR     1.016  0.456  2.166 1.000              1.000
label_platinum residual_subopt 252        82              OR     1.116  0.586  2.090 0.762              0.914
label_platinum      aneuploidy 265        82 rank-biserial r     0.125    NaN    NaN 0.103              0.207
label_platinum             tmb 255        79 rank-biserial r    -0.157    NaN    NaN 0.043              0.130
label_platinum             age 277        87 rank-biserial r     0.072    NaN    NaN 0.337              0.505
label_pfiplat6        brca_mut 272        82              OR     0.000  0.000  0.332 0.000              0.001
label_pfiplat6        stage_iv 388       115              OR     1.088  0.567  2.028 0.762              0.762
label_pfiplat6 residual_subopt 310        96              OR     1.251  0.709  2.184 0.415              0.498
label_pfiplat6      aneuploidy 373       109 rank-biserial r     0.211    NaN    NaN 0.001              0.004
label_pfiplat6             tmb 354       104 rank-biserial r    -0.057    NaN    NaN 0.397              0.498
label_pfiplat6             age 389       115 rank-biserial r     0.146    NaN    NaN 0.023              0.046
label_response        brca_mut 303        48              OR     1.231  0.345  3.580 0.782              0.782
label_response        stage_iv 424        65              OR     1.251  0.571  2.566 0.579              0.782
label_response residual_subopt 335        52              OR     2.549  1.314  4.912 0.003              0.021
label_response      aneuploidy 409        64 rank-biserial r    -0.031    NaN    NaN 0.696              0.782
label_response             tmb 391        63 rank-biserial r    -0.028    NaN    NaN 0.720              0.782
label_response             age 425        65 rank-biserial r     0.060    NaN    NaN 0.441              0.782
    label_os18        brca_mut 126        10              OR     0.000  0.000  5.593 1.000              1.000
    label_os18        stage_iv 206        22              OR     1.224  0.214  4.711 0.727              0.872
    label_os18 residual_subopt 180        17              OR     3.604  1.159 11.883 0.014              0.041
    label_os18      aneuploidy 198        22 rank-biserial r     0.416    NaN    NaN 0.001              0.009
    label_os18             tmb 199        21 rank-biserial r    -0.105    NaN    NaN 0.423              0.634
    label_os18             age 206        22 rank-biserial r     0.288    NaN    NaN 0.027              0.055
    label_os24        brca_mut 123        17              OR     0.000  0.000  2.806 0.354              0.425
    label_os24        stage_iv 199        36              OR     0.894  0.208  2.932 1.000              1.000
    label_os24 residual_subopt 174        30              OR     2.263  0.930  5.473 0.052              0.103
    label_os24      aneuploidy 191        36 rank-biserial r     0.326    NaN    NaN 0.002              0.014
    label_os24             tmb 192        34 rank-biserial r    -0.115    NaN    NaN 0.283              0.425
    label_os24             age 199        36 rank-biserial r     0.222    NaN    NaN 0.037              0.103
```

## Predictions vs observed

- P1 BRCA, label_platinum: OR 0.00 [0.00, 0.53], p = 0.0033, q = 0.0198 (cov=1: 0.0/16.0 label=1; cov=0: 59.0/175.0)
- P1 BRCA, label_pfiplat6: OR 0.00 [0.00, 0.33], p = 0.000122, q = 0.000732 (cov=1: 0.0/25.0 label=1; cov=0: 82.0/247.0)
- P2 BRCA, label_os18: OR 0.00 [0.00, 5.59], p = 1, q = 1 (cov=1: 0.0/10.0 label=1; cov=0: 10.0/116.0)
- P2 BRCA, label_os24: OR 0.00 [0.00, 2.81], p = 0.354, q = 0.425 (cov=1: 0.0/10.0 label=1; cov=0: 17.0/113.0)
- (BRCA, label_response: OR 1.23 [0.35, 3.58], p = 0.782, q = 0.782 (cov=1: 5.0/27.0 label=1; cov=0: 43.0/276.0))
- P3 residual, label_platinum: OR 1.12 [0.59, 2.09], p = 0.762, q = 0.914 (cov=1: 23.0/67.0 label=1; cov=0: 59.0/185.0)
- P4 age, label_os24: r = +0.222, medians 59 vs 57, p = 0.037, q = 0.103, n = 199; label_platinum: r = +0.072, medians 60 vs 58, p = 0.337, q = 0.505, n = 277
- P5 aneuploidy/TMB, smallest q: label_platinum 0.13, label_pfiplat6 0.00399, label_response 0.782, label_os18 0.00888, label_os24 0.0141
- P6 stage IV ORs: label_platinum 1.02 [0.46, 2.17], label_pfiplat6 1.09 [0.57, 2.03], label_response 1.25 [0.57, 2.57], label_os18 1.22 [0.21, 4.71], label_os24 0.89 [0.21, 2.93]

## Decision rule (BRCA known-groups validity)

- label_platinum: **BRCA-valid**
- label_pfiplat6: **BRCA-valid**
- label_response: **not supported**
- label_os18: **direction only**
- label_os24: **direction only**

Supplement: label_os12 rows in a3_known_groups.csv (supplement = True). Covariates per patient: a3_covariates.csv.
## Post-run notes (added after the run; header predictions left unchanged)

- **Prediction scorecard:** P1 held (both platinum labels BRCA-valid; 0/16 and 0/25 BRCA mutants resistant). P2 failed as worded: OS-label ORs are also 0 (0/10 mutants non-responders), not "closer to 1"; their CIs include 1 because only 10 of the BRCA-sequenced OS-labelled patients are mutant and non-responders are rare (OS18: 10/126; OS24: 17/123), so fewer than 2 mutant non-responders would be expected even with no association — the BRCA test is uninformative for OS labels, not evidence against them. P3 failed (OR 1.12). P4 held (age r +0.22 for OS24, +0.07 for platinum). P5 failed: aneuploidy is BH-significant for label_pfiplat6 (q 0.004), label_os18 (q 0.009) and label_os24 (q 0.014), not for label_platinum (q 0.21) or label_response. P6 failed as worded (OS24 OR 0.89); every stage-IV CI includes 1.
- **Correction to the header's disclosure (P3):** TCGA 2011 SI Methods S1 (section "Surgical outcome is associated with OS, PFS, and platinum status") states verbatim: "We found no association between platinum status and surgical cytoreduction when defined traditionally as optimal or suboptimal." The association it reports is for microscopic residual disease vs more than microscopic ("P = 0.003, df=2, Odds ratio = 3.1"). The header summarised this loosely; the observed OR 1.12 for optimal vs suboptimal reproduces TCGA's own null. Microscopic-only was not pre-specified and is not tested here.
- **Pattern (descriptive):** residual disease is associated with label_response (OR 2.55, q 0.021) and label_os18 (OR 3.60, q 0.041) but not label_platinum; aneuploidy with OS labels and the PFI-from-platinum label but not the published platinum label.

## A3 part 2 — PFI Cox (03b_pfi_cox.R, run by Aaron on host R 4.6.0, 2026-10-29)

v2 Cox cohort (n = 432, 317 PFI events; BRCA subset 335, 28 mutant). Endpoint CDR PFI; formula unchanged from phase2/src/hrd. One pre-run bug fix (cox.zph could not rebuild the model frame; `coxph` now called via `do.call`) — no change to models or predictions.

| Model | Term | HR [95% CI] | p |
|---|---|---|---|
| baseline, full (n 432) | aneuploidy | 1.028 [1.012, 1.043] | 0.00045 |
| | log1p(TMB) | 0.897 [0.762, 1.056] | 0.19 |
| baseline, matched (n 335) | aneuploidy | 1.029 [1.010, 1.048] | 0.0028 |
| | log1p(TMB) | 0.693 [0.519, 0.926] | 0.013 |
| BRCA added (n 335) | BRCA_any_mutated | 0.499 [0.287, 0.869] | 0.014 |
| | aneuploidy | 1.026 [1.007, 1.045] | 0.0062 |
| | log1p(TMB) | 0.762 [0.565, 1.027] | 0.074 |

C-index: 0.560 (full baseline), 0.562 (matched baseline), 0.574 (BRCA added). Global Schoenfeld p: 0.958 / 0.634 / 0.722.

Scorecard: P1 held (aneuploidy HR > 1, p < 0.05; TMB CI includes 1 in the full cohort). P2 partly failed: BRCA HR 0.499 (p 0.014) is < 1 as predicted but not lower than the v2 OS estimate (0.455). P3 held (C-index 0.560). P4 held (global Schoenfeld p 0.958; the BRCA term also meets PH for PFI, p 0.68, unlike the borderline p 0.042 for OS in v2).

# A3b: Cox models of the progression-free interval

*Status:* pre-specified. *Script:* `label_validity/03b_pfi_cox.R`.

## Header (verbatim)

```text
============================================================
 label_validity/03b_pfi_cox.R
 Q2 analysis A3, part 2 — Cox model for PFI (time to progression)
 (claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A3)

 Reuses the v2 Cox code with ONLY the endpoint swapped:
   * phase2/phase2_02_cox_model.R  — cohort and covariates (log1p(TMB) + aneuploidy)
   * src/hrd/02_cox_model_with_brca.R — BRCA merge and baseline-vs-BRCA comparison
 Cohort: phase2/outputs/cox_patients_with_risk.csv (n = 432; platinum = AGENT
   matching "platin", so it includes TCGA-29-1711, oxaliplatin only — one patient
   more than the classification cohort; same cohort as the v2 OS Cox model).
 Endpoint: TCGA-CDR PFI / PFI.time (days from diagnosis → months / 30.4375),
   from label_validity/outputs/cdr_ov_pfi.csv (exported from
   TCGA-CDR-SupplementalTableS1.xlsx, sheet TCGA-CDR, type == "OV").

 Run from project root on the host:
   "C:\Program Files\R\R-4.6.0\bin\Rscript.exe" label_validity\03b_pfi_cox.R

 Outputs → label_validity/outputs/
   a3_pfi_cox_hr.csv       HRs, 95% CI, p for all models
   a3_pfi_cox_summary.csv  n, events, C-index per model
   a3_pfi_cox_ph.csv       Schoenfeld tests per model

 ============================================================
 PREDICTIONS (written 2026-10-29 before running — DEC-019)
 ============================================================
 Already seen (disclosed): A3 part 1 found BRCA mutants 0/25 PFI-from-platinum
 resistant and aneuploidy higher in PFI-from-platinum-resistant patients
 (r = +0.21, q = 0.004). v2 OS Cox: aneuploidy HR 1.021 (p 0.017), TMB HR 0.894
 (p 0.238), C-index 0.570; BRCA HR 0.455 (p 0.024), n = 335.
   P1  Baseline PFI model (n ≈ 432): aneuploidy HR > 1 with p < 0.05;
       log1p(TMB) HR CI includes 1.
   P2  BRCA model (matched subset ≈ 335): BRCA_any_mutated HR < 1 with p < 0.05,
       and its HR is lower than the v2 OS estimate (0.455).
   P3  Baseline PFI C-index between 0.53 and 0.62.
   P4  Global Schoenfeld p > 0.05 for the baseline model.
 No multiplicity correction: 3 pre-specified models, each reported in full.
 ============================================================
```

# A4: transfer to GSE63885

*Status:* pre-specified. *Script:* `label_validity/04_transfer_matrix.py`. *Summary:* `label_validity/outputs/04_transfer_summary.md`.

## Header (verbatim)

```text
label_validity/04_transfer_matrix.py
────────────────────────────────────
Q2 analysis A4 — label-transfer matrix
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A4).

Question: does a classifier trained on TCGA-OV with a platinum-response label
transfer to GSE63885 better than one trained on an OS-threshold label?

DESIGN — validation/06_external_validation_v2.py with ONLY the training label
swapped. Everything else is copied unchanged: common-gene restriction, top 500
variance genes selected in the TCGA training set per label, variant P (primary:
log2(RSEM+1), TCGA scaler fit on training data, GEO z-scored within GEO) and
variant S (sensitivity: raw RSEM as in the paper), LR/RF/SVM from
config/config.yaml (seed 42), GEO test labels `clinical` (SD/PD vs CR/PR) and
`dfs` (platinum-resistant DFS < 180 d vs sensitive), AUC with 2,000-resample
stratified bootstrap CI (seed 42). GSE63885 is never used for fitting or selection.

Training labels (from label_validity/outputs/labels_master.csv, A1):
  label_platinum (primary), label_pfiplat6, label_response, label_os18, label_os24;
  label_os12 kept only for the reproduction check (supplement).
  Each label is turned into the {PATIENT_ID, response} frame that
  src.preprocessing.align_expression_to_labels expects, so patient alignment and
  ordering are identical to 06.

Run on the host (sklearn 1.9.0):
  C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe label_validity\\04_transfer_matrix.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"

Outputs → label_validity/outputs/a4_transfer_results.csv, 04_transfer_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already known (disclosed): v2 OS-trained results
(validation/outputs/external_validation_v2_results.csv), variant P, dfs label:
12m 0.498–0.536, 18m 0.545–0.581, 24m 0.610–0.674; clinical label 0.480–0.575;
1 of 36 CIs excluded 0.5. A1 training n: platinum 145 (41 resistant),
pfiplat6 188 (53), response 219 (35), OS18 206 (22), OS24 199 (36).

  C1  REPRODUCTION CHECK: rows for label_os12/os18/os24 equal the v2 results
      file (all 36 AUCs and CIs to 4 dp). If not, the harness changed and the
      remaining rows are not interpretable until explained.
  P1  Variant P, dfs label: mean AUC over the 3 models for label_platinum is
      higher than for label_os18 and higher than for label_os24.
  P2  All variant-P AUCs (5 main labels × 3 models × 2 GEO labels = 30) < 0.70.
  P3  At most 3 of those 30 variant-P CIs exclude 0.5.
  P4  GEO clinical label (10 non-responders): every variant-P CI includes 0.5.
  P5  Variant S mean AUC ≤ variant P mean AUC for the platinum-trained models.

DECISION RULE (pre-specified):
  "Label choice improves transfer" if, in variant P on the dfs label,
  label_platinum or label_pfiplat6 has ≥ 2 of 3 models with CI excluding 0.5
  AND its mean AUC exceeds both OS labels' means.
  Otherwise: "transfer remains weak whatever the training label"; A5 then
  separates label mismatch from platform mismatch within TCGA.
```

## Summary: results and scorecard (verbatim)

# A4 — label-transfer matrix (TCGA-OV → GSE63885)

sklearn 1.9.0; common genes 15994. Harness = validation/06_external_validation_v2.py, training label swapped.

C1 reproduction: 36/36 rows matched; max |Δ| = 0.16010 → **FAIL — stop and explain before interpreting**

## Variant P (primary): AUC by training label × model × GEO label

```
label                               clinical    dfs
train_label    model                               
label_platinum Logistic Regression     0.616  0.563
               Random Forest           0.712  0.588
               SVM                     0.689  0.616
label_pfiplat6 Logistic Regression     0.670  0.552
               Random Forest           0.745  0.625
               SVM                     0.706  0.610
label_response Logistic Regression     0.630  0.558
               Random Forest           0.547  0.561
               SVM                     0.627  0.574
label_os18     Logistic Regression     0.508  0.581
               Random Forest           0.421  0.555
               SVM                     0.550  0.545
label_os24     Logistic Regression     0.505  0.622
               Random Forest           0.484  0.645
               SVM                     0.575  0.610
```

Full table with 95% CIs: a4_transfer_results.csv.

## Predictions vs observed

- P1 mean dfs AUC (variant P) by training label: label_platinum 0.589, label_pfiplat6 0.596, label_response 0.564, label_os18 0.560, label_os24 0.626 → platinum > OS18 and > OS24: False
- P2 max variant-P AUC: 0.745 (predicted all < 0.70)
- P3 variant-P CIs excluding 0.5: 5 of 30 (predicted ≤ 3); label_platinum/Random Forest/clinical 0.712 [0.559, 0.843]; label_platinum/SVM/clinical 0.689 [0.509, 0.845]; label_pfiplat6/Random Forest/clinical 0.745 [0.591, 0.880]; label_pfiplat6/SVM/clinical 0.706 [0.541, 0.858]; label_os24/Random Forest/dfs 0.645 [0.522, 0.772]
- P4 clinical label CIs excluding 0.5: 4 (predicted 0)
- P5 platinum-trained mean AUC: variant S 0.642 vs variant P 0.631 (predicted S ≤ P)

**Decision rule: Transfer remains weak whatever the training label.** dfs CIs excluding 0.5 per label: label_platinum 0/3, label_pfiplat6 0/3, label_response 0/3, label_os18 0/3, label_os24 1/3
## Post-run notes (added after the run; header predictions unchanged)

### C1 failure — explained
- Only the 12 Random Forest rows differed from `validation/outputs/external_validation_v2_results.csv` (max |Δ| 0.160); all 24 LR and SVM rows matched exactly (Δ = 0.000), so data, gene selection, labels and patient alignment are identical.
- `validation/outputs/external_validation_v2_summary.md` records **"sklearn 1.7.2"**: the v2 external validation was run in an earlier session's VM, not in the pinned host environment (sklearn 1.9.0).
- `04a_rf_determinism_check.py` (same code, same data, 12m / variant S / clinical): host Python 3.14.5 + sklearn 1.9.0 + numpy 2.4.6 → AUC 0.4711 in 6/6 fits (n_jobs −1 and 1); VM Python 3.10.12 + sklearn 1.7.2 + numpy 2.2.6 → 0.6312 in 6/6 fits = the v2 value. Both environments are deterministic; RF output differs between the two sklearn versions. (`04a_rf_determinism.txt`, `04a_rf_determinism_VM.txt`.)
- Conclusion: the harness did not change; the reference file was produced under a different sklearn version. A4 (host, pinned 1.9.0) is interpretable. **Consequence for v2:** the RF rows of the v2 external validation (S1 Table, manuscript text) are from sklearn 1.7.2 and must be replaced by the pinned-environment values — the label_os12/18/24 rows of `a4_transfer_results.csv`.

### Prediction scorecard (variant P)
- P1 failed: mean dfs AUC platinum 0.589, pfiplat6 0.596, response 0.564, OS18 0.560, **OS24 0.626** (highest).
- P2 failed: max AUC 0.745 (pfiplat6 / RF / clinical).
- P3 failed: 5 of 30 CIs exclude 0.5 (predicted ≤ 3).
- P4 failed: 4 clinical-label CIs exclude 0.5 (predicted 0) — all four from platinum-trained models: platinum RF 0.712 [0.559, 0.843], platinum SVM 0.689 [0.509, 0.845], pfiplat6 RF 0.745 [0.591, 0.880], pfiplat6 SVM 0.706 [0.541, 0.858]. OS-trained models on the clinical label: 0.421–0.575, all CIs include 0.5.
- P5 failed narrowly: platinum-trained mean AUC variant S 0.642 vs P 0.631.
- **Pre-specified decision (dfs label): "Transfer remains weak whatever the training label"** — no platinum-trained model has a dfs CI excluding 0.5; the one dfs CI excluding 0.5 is OS24 / RF (0.645 [0.522, 0.772]).

### Not pre-specified (report as observed, not as a finding)
- On the GEO clinical label (SD/PD vs CR/PR; 10 non-responders, all DFS-resistant per G4), platinum-trained models scored 0.616–0.745 and OS-trained 0.421–0.575. The decision rule was set on the dfs label, the clinical label has 10 events, and the 30 variant-P AUCs are uncorrected; this pattern is descriptive only.

# A5: within-TCGA cross-label CV

*Status:* pre-specified; after external review reported as descriptive only, and its decision rule is superseded by the controlled comparison (A16). *Script:* `label_validity/05_cross_label_cv.py`. *Summary:* `label_validity/outputs/05_cross_label_summary.md`.

## Header (verbatim)

```text
label_validity/05_cross_label_cv.py
───────────────────────────────────
Q2 analysis A5 — within-TCGA cross-label prediction
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, A5).

Question: inside TCGA-OV alone, do models trained on one label predict another
label in held-out patients? This separates "label mismatch" from "platform /
cohort mismatch" as the cause of the weak transfer seen in A4.

DESIGN (fixed before running)
  Patients: platinum-treated with RNA-seq (labels_master.csv, in_rnaseq; n = 251).
  Labels: label_platinum (primary), label_pfiplat6 (sensitivity), label_os18,
    label_os24. 4 training labels × 4 test labels; the diagonal is each label's
    own cross-validated ceiling.
  Folds: StratifiedKFold(5, shuffle) on all 251 patients, stratified on
    label_platinum with undetermined as its own stratum; 5 repeats (seeds 0–4).
  Per fold and training label: train on fold-train patients whose training
    label is determinate. Inside that training set only: log2(RSEM + 1), top 500
    genes by variance (genes restricted to the 15,994 symbols common with
    GSE63885, exactly as A4), StandardScaler fit; transform the test fold.
    Models LR / RF / SVM from config/config.yaml (seed 42). Hyperparameters are
    fixed, so there is no inner tuning loop — selection and scaling inside each
    training fold is the whole of the nesting.
  Each fitted model scores every test-fold patient; per repeat, out-of-fold
  scores are pooled and one AUC is computed for each test label on the patients
  where that label is determinate. Reported: mean AUC over the 5 repeats with
  min–max.
  Same preprocessing as A4's primary variant (P), so A5's diagonal is
  comparable with A4's GEO AUCs.

Run on the host (sklearn 1.9.0), from the project root:
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\05_cross_label_cv.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Outputs → label_validity/outputs/a5_cross_label_repeats.csv, 05_cross_label_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Already known (disclosed): v2 clean within-TCGA AUC (raw RSEM, single split,
30 repeats): 18m 0.62–0.67, 24m 0.68–0.73 by model. A4 GEO dfs AUC, mean of 3
models: platinum-trained 0.589, OS24-trained 0.626. A2: κ(OS18, platinum) 0.14,
κ(OS24, platinum) 0.25, κ(platinum, pfiplat6) 0.97.

  P1  Diagonal: OS24 → OS24 mean AUC (mean of 3 models) 0.62–0.72;
      platinum → platinum 0.52–0.65.
  P2  OS-trained → platinum: mean AUC (OS18 and OS24, 3 models) ≤ 0.58.
  P3  platinum-trained → OS24: mean AUC ≤ 0.60.
  P4  platinum ↔ pfiplat6 off-diagonal within 0.03 of the corresponding diagonal.

DECISION RULE (all quantities = mean over 3 models and 5 repeats):
  ceiling  = AUC(platinum → platinum)
  label    = ceiling − mean[AUC(OS18 → platinum), AUC(OS24 → platinum)]
  platform = ceiling − 0.589 (A4: platinum-trained, GEO dfs label)
  If ceiling < 0.55: "platinum status is not predictable from expression within
    TCGA at this sample size; label and platform effects cannot be separated".
  Otherwise: label mismatch supported if label ≥ 0.05; platform/cohort shift
    supported if platform ≥ 0.05 (both can hold).
```

## Summary: results and scorecard (verbatim)

# A5 — within-TCGA cross-label prediction

sklearn 1.9.0; 251 platinum-treated patients with RNA-seq; 15994 common genes; 5 × 5-fold CV, pooled out-of-fold AUC per repeat. Variant P preprocessing (as A4).

## Mean AUC over 3 models × 5 repeats (rows = training label, columns = test label)

```
test_label      label_platinum  label_pfiplat6  label_os18  label_os24
train_label                                                           
label_platinum           0.634           0.617       0.578       0.630
label_pfiplat6           0.593           0.608       0.592       0.623
label_os18               0.552           0.585       0.631       0.651
label_os24               0.597           0.618       0.675       0.682
```

## Per model: mean [min, max] over repeats

```
   train_label     test_label               model  mean   min   max
    label_os18     label_os18 Logistic Regression 0.668 0.647 0.688
    label_os18     label_os18       Random Forest 0.631 0.601 0.664
    label_os18     label_os18                 SVM 0.594 0.568 0.619
    label_os18     label_os24 Logistic Regression 0.675 0.630 0.696
    label_os18     label_os24       Random Forest 0.654 0.586 0.699
    label_os18     label_os24                 SVM 0.624 0.531 0.666
    label_os18 label_pfiplat6 Logistic Regression 0.597 0.580 0.634
    label_os18 label_pfiplat6       Random Forest 0.581 0.541 0.612
    label_os18 label_pfiplat6                 SVM 0.578 0.553 0.598
    label_os18 label_platinum Logistic Regression 0.574 0.560 0.603
    label_os18 label_platinum       Random Forest 0.542 0.493 0.597
    label_os18 label_platinum                 SVM 0.540 0.509 0.563
    label_os24     label_os18 Logistic Regression 0.707 0.636 0.751
    label_os24     label_os18       Random Forest 0.659 0.621 0.672
    label_os24     label_os18                 SVM 0.661 0.622 0.700
    label_os24     label_os24 Logistic Regression 0.708 0.627 0.756
    label_os24     label_os24       Random Forest 0.674 0.599 0.706
    label_os24     label_os24                 SVM 0.663 0.586 0.720
    label_os24 label_pfiplat6 Logistic Regression 0.603 0.568 0.641
    label_os24 label_pfiplat6       Random Forest 0.628 0.593 0.660
    label_os24 label_pfiplat6                 SVM 0.621 0.602 0.632
    label_os24 label_platinum Logistic Regression 0.593 0.561 0.620
    label_os24 label_platinum       Random Forest 0.603 0.572 0.650
    label_os24 label_platinum                 SVM 0.597 0.577 0.605
label_pfiplat6     label_os18 Logistic Regression 0.577 0.567 0.583
label_pfiplat6     label_os18       Random Forest 0.603 0.580 0.615
label_pfiplat6     label_os18                 SVM 0.596 0.562 0.624
label_pfiplat6     label_os24 Logistic Regression 0.585 0.581 0.593
label_pfiplat6     label_os24       Random Forest 0.651 0.630 0.680
label_pfiplat6     label_os24                 SVM 0.632 0.594 0.665
label_pfiplat6 label_pfiplat6 Logistic Regression 0.597 0.571 0.623
label_pfiplat6 label_pfiplat6       Random Forest 0.610 0.569 0.627
label_pfiplat6 label_pfiplat6                 SVM 0.616 0.590 0.634
label_pfiplat6 label_platinum Logistic Regression 0.594 0.569 0.614
label_pfiplat6 label_platinum       Random Forest 0.592 0.549 0.620
label_pfiplat6 label_platinum                 SVM 0.592 0.543 0.629
label_platinum     label_os18 Logistic Regression 0.560 0.539 0.600
label_platinum     label_os18       Random Forest 0.580 0.526 0.632
label_platinum     label_os18                 SVM 0.593 0.567 0.640
label_platinum     label_os24 Logistic Regression 0.612 0.597 0.637
label_platinum     label_os24       Random Forest 0.637 0.586 0.686
label_platinum     label_os24                 SVM 0.640 0.608 0.692
label_platinum label_pfiplat6 Logistic Regression 0.621 0.592 0.656
label_platinum label_pfiplat6       Random Forest 0.610 0.583 0.659
label_platinum label_pfiplat6                 SVM 0.619 0.583 0.654
label_platinum label_platinum Logistic Regression 0.650 0.620 0.686
label_platinum label_platinum       Random Forest 0.627 0.564 0.689
label_platinum label_platinum                 SVM 0.625 0.582 0.671
```

## Predictions vs observed

- P1 diagonal: OS24→OS24 0.682 (predicted 0.62–0.72); platinum→platinum 0.634 (predicted 0.52–0.65)
- P2 OS-trained → platinum: OS18 0.552, OS24 0.597, mean 0.575 (predicted ≤ 0.58)
- P3 platinum → OS24: 0.630 (predicted ≤ 0.60)
- P4 platinum→pfiplat6 0.617 vs pfiplat6→pfiplat6 0.608; pfiplat6→platinum 0.593 vs platinum→platinum 0.634 (predicted within 0.03)

Ceiling 0.634; label effect +0.060; platform effect +0.045 (vs A4 GEO dfs 0.589).
**Decision rule: label mismatch SUPPORTED; platform/cohort shift not supported.**
## Post-run notes (added after the run; header predictions unchanged)

Run by Aaron on the host (sklearn 1.9.0), 2026-10-29 16:35 ET. A VM dry run (sklearn 1.7.2, 1 repeat) was made after the predictions were committed, as a smoke test only; its numbers are not used.

### Scorecard
- P1 held: OS24→OS24 0.682 (0.62–0.72); platinum→platinum 0.634 (0.52–0.65).
- P2 held, barely: OS-trained → platinum 0.575 (≤ 0.58); OS18 0.552, OS24 0.597.
- P3 failed: platinum → OS24 0.630 (predicted ≤ 0.60) — close to OS24's own ceiling (0.682).
- P4 failed: pfiplat6→platinum 0.593 vs ceiling 0.634 (Δ 0.041 > 0.03); platinum→pfiplat6 0.617 exceeds pfiplat6→pfiplat6 0.608.

### Stability of the decision-rule quantities across the 5 repeats (mean of 3 models)
- Ceiling (platinum→platinum): 0.653, 0.645, 0.605, 0.679, 0.590.
- Label effect: 0.091, 0.074, 0.019, 0.084, 0.030 — ≥ 0.05 in 3 of 5 repeats; mean +0.060.
- Platform effect (vs A4 0.589): 0.064, 0.056, 0.016, 0.090, 0.001 — ≥ 0.05 in 3 of 5 repeats; mean +0.045.
- The pre-specified verdict on the means ("label mismatch supported; platform/cohort shift not supported") rests on a 0.015 difference between two small effects whose repeat-to-repeat ranges overlap. Reportable wording: both effects are small (≈ 0.05 AUC) and neither is robust; the binding constraint is the low within-TCGA ceiling for platinum status (0.634), so expression predicts platinum status only modestly even before any label or platform shift.
- The platform comparison is crude by design: A4 trained on all 145 labelled patients, A5 on ≈ 116 per fold, and they are scored on different cohorts.

# A6: published gene sets

*Status:* pre-specified (supplementary). *Script:* `label_validity/06_published_genesets.py`. *Summary:* `label_validity/outputs/06_published_genesets_summary.md`.

## Header (verbatim)

```text
label_validity/06_published_genesets.py
───────────────────────────────────────
Q2 analysis A6 (supplementary) — published gene sets as fixed inputs
(claude/HANDOFF_Ovarian_Q2_Reorg_2026-10-29.md §4, optional A6; Aaron chose to run it 2026-10-29).

Question: used as fixed inputs to this project's leakage-free pipeline, do two
published platinum-response gene sets predict platinum status better than
random gene sets of the same size?
FRAMING (fixed): this evaluates the gene LISTS as fixed inputs to OUR pipeline.
It is not a reproduction of either paper's pipeline (both are under-specified)
and says nothing about the original authors' reported performance.

Gene sets (verified from the local PDFs, 2026-10-29)
  Chen et al. 2022, J Ovarian Res 15:39, Discussion: "The classifier comprised of 10 genes
    (CD209, CD274, HIST1H3I, HIST1H4L, NLGN1, NTRK3, PNLDC1, SLC22A3, SLC5A1 and SYNM)".
  Gao et al. 2025, Sci Rep 15:19123, Abstract: "5 genes (PAX2, TFPI2, APOA1, ADIRF and CRISP3)".
Symbol mapping (HGNC records, checked 2026-10-29): HIST1H3I = H3C11, HIST1H4L = H4C13
  (GSE63885 file uses the new symbols; TCGA the old); ADIRF previous symbol C10orf116
  (TCGA uses C10orf116, GSE63885 ADIRF). All 15 genes are present on both platforms.

DESIGN (fixed before running)
  Training labels: label_platinum (primary), label_pfiplat6 (secondary), from labels_master.csv,
    platinum-treated patients with RNA-seq.
  Preprocessing (as A4/A5 variant P): TCGA log2(RSEM + 1); StandardScaler fit on training rows
    only; GSE63885 genes z-scored within GEO. No gene selection — the set IS the feature set.
  Endpoints:
    E1  within TCGA: StratifiedKFold(5, shuffle) on patients with the label determinate,
        5 repeats (seeds 0–4); pooled out-of-fold AUC per repeat; mean over repeats.
    E2  transfer: train on all labelled TCGA patients; AUC on GSE63885 dfs label
        (34 resistant / 40 sensitive) — primary transfer endpoint, as in A4.
    E3  transfer: as E2, GSE63885 clinical label (10 / 64) — secondary.
  Null: 1,000 random gene sets per set size (10 and 5) drawn without replacement from the
    symbols common to both platforms that have no missing values in either matrix for the
    patients/samples used (seed 2026; restriction added after a 20-draw VM smoke test hit NaN
    expression values, before any real run); the same random sets are used for
    every label and endpoint; same folds as the published sets.
  Model for the null comparison: Logistic Regression from config/config.yaml (seed 42).
  Random Forest and SVM are reported for the published sets only (descriptive, no null).
  Empirical one-sided p = (1 + #random AUC ≥ published AUC) / 1001.
  Multiplicity: Benjamini–Hochberg across the 12 tests (2 sets × 2 labels × 3 endpoints).

Run on the host (sklearn 1.9.0), from the project root:
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\06_published_genesets.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Outputs → label_validity/outputs/a6_published_sets.csv, a6_null.csv, 06_published_genesets_summary.md

══════════════════════════════════════════════════════════════════════════════
PREDICTIONS (written 2026-10-29 before running — DEC-019)
══════════════════════════════════════════════════════════════════════════════
Design facts behind them (stated, not judged): Chen et al. selected their 10 genes on TCGA-OV
patients labelled by PFI < 6 months (n = 230), using the full labelled set; those patients very
likely overlap ours (patient IDs not published, overlap not verifiable). Gao et al. took
candidate genes from an external single-cell dataset; the gene count was chosen on pooled
TCGA + GEO data. A5 ceiling for platinum status with 500 variance-selected genes: 0.634.

  P1  Chen set, E1, label_platinum: empirical p < 0.05 (the genes were chosen on overlapping
      TCGA patients, so within-TCGA evaluation is expected to look better than random).
  P2  Chen set, E2 (GEO dfs), label_platinum: empirical p ≥ 0.05.
  P3  Gao set, E1, label_platinum: empirical p ≥ 0.05.
  P4  Gao set, E2, label_platinum: empirical p ≥ 0.05.
  P5  Median random-set E1 AUC (LR, label_platinum): 0.50–0.58 for both set sizes.
  P6  No published-set LR AUC on any endpoint exceeds 0.75.

DECISION RULE: a published set "predicts better than random gene sets of the same size" on an
endpoint only if BH q < 0.05. Otherwise it is reported as "not distinguishable from random gene
sets of the same size under this evaluation".
```

## Summary: results and scorecard (verbatim)

# A6 — published gene sets as fixed inputs (supplementary)

sklearn 1.9.0; 251 platinum-treated patients with RNA-seq; null = 1000 random same-size sets from 15484 common genes. Evaluates the gene LISTS in this pipeline; not a reproduction of either paper's pipeline.

## LR vs random gene sets (BH across 12 tests)

```
   gene_set          label        endpoint  auc_lr  null_median  null_p95  n_null  p_emp  q_bh  better_than_random
Chen2022_10 label_platinum      E1_tcga_cv   0.735        0.500     0.599    1000  0.001 0.006                True
Chen2022_10 label_platinum      E2_geo_dfs   0.499        0.525     0.628    1000  0.645 0.705               False
Chen2022_10 label_platinum E3_geo_clinical   0.530        0.526     0.684    1000  0.493 0.705               False
Chen2022_10 label_pfiplat6      E1_tcga_cv   0.687        0.521     0.608    1000  0.001 0.006                True
Chen2022_10 label_pfiplat6      E2_geo_dfs   0.485        0.529     0.640    1000  0.754 0.754               False
Chen2022_10 label_pfiplat6 E3_geo_clinical   0.514        0.541     0.706    1000  0.603 0.705               False
  Gao2025_5 label_platinum      E1_tcga_cv   0.537        0.498     0.604    1000  0.271 0.705               False
  Gao2025_5 label_platinum      E2_geo_dfs   0.501        0.513     0.624    1000  0.567 0.705               False
  Gao2025_5 label_platinum E3_geo_clinical   0.492        0.520     0.694    1000  0.590 0.705               False
  Gao2025_5 label_pfiplat6      E1_tcga_cv   0.517        0.511     0.608    1000  0.461 0.705               False
  Gao2025_5 label_pfiplat6      E2_geo_dfs   0.521        0.524     0.628    1000  0.520 0.705               False
  Gao2025_5 label_pfiplat6 E3_geo_clinical   0.486        0.536     0.703    1000  0.646 0.705               False
```

## All models, published sets only (descriptive)

```
endpoint                                        E1_tcga_cv  E2_geo_dfs  E3_geo_clinical
gene_set    label          model                                                       
Chen2022_10 label_pfiplat6 Logistic Regression       0.687       0.485            0.514
                           Random Forest             0.646       0.541            0.470
                           SVM                       0.645       0.482            0.536
            label_platinum Logistic Regression       0.735       0.499            0.530
                           Random Forest             0.716       0.575            0.541
                           SVM                       0.676       0.503            0.536
Gao2025_5   label_pfiplat6 Logistic Regression       0.517       0.521            0.486
                           Random Forest             0.492       0.435            0.451
                           SVM                       0.486       0.586            0.516
            label_platinum Logistic Regression       0.537       0.501            0.492
                           Random Forest             0.508       0.463            0.504
                           SVM                       0.451       0.422            0.430
```

## Predictions vs observed

- P1 Chen, E1, platinum: AUC 0.735 vs random median 0.500 (95th pct 0.599), p = 0.001, q = 0.006 (predicted p < 0.05)
- P2 Chen, E2, platinum: AUC 0.499 vs random median 0.525 (95th pct 0.628), p = 0.645, q = 0.705 (predicted p ≥ 0.05)
- P3 Gao, E1, platinum: AUC 0.537 vs random median 0.498 (95th pct 0.604), p = 0.271, q = 0.705 (predicted p ≥ 0.05)
- P4 Gao, E2, platinum: AUC 0.501 vs random median 0.513 (95th pct 0.624), p = 0.567, q = 0.705 (predicted p ≥ 0.05)
- P5 random-set median E1 AUC, platinum: size 5 0.498, size 10 0.500 (predicted 0.50–0.58)
- P6 max published-set LR AUC on any endpoint: 0.735 (predicted ≤ 0.75)

## Decision rule (BH q < 0.05)

- Chen2022_10 / label_platinum / E1_tcga_cv: **better than random gene sets of the same size**
- Chen2022_10 / label_platinum / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Chen2022_10 / label_platinum / E3_geo_clinical: not distinguishable from random gene sets of the same size
- Chen2022_10 / label_pfiplat6 / E1_tcga_cv: **better than random gene sets of the same size**
- Chen2022_10 / label_pfiplat6 / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Chen2022_10 / label_pfiplat6 / E3_geo_clinical: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_platinum / E1_tcga_cv: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_platinum / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_platinum / E3_geo_clinical: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_pfiplat6 / E1_tcga_cv: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_pfiplat6 / E2_geo_dfs: not distinguishable from random gene sets of the same size
- Gao2025_5 / label_pfiplat6 / E3_geo_clinical: not distinguishable from random gene sets of the same size
## Post-run notes (added after the run; header predictions unchanged)

Run by Aaron on the host (sklearn 1.9.0), 2026-10-29 ~17:05 ET. One pre-run design fix: null pool restricted to genes with complete data (15,484 of 15,994), after a 20-draw VM smoke test hit NaN values; smoke-test results were not inspected.

### Scorecard
- P1 held: Chen set within TCGA, platinum label, LR AUC 0.735 vs random median 0.500 (95th pct 0.599); p = 0.001 (no random set reached it), q = 0.006. Same for PFI-from-platinum: 0.687, q = 0.006.
- P2 held: Chen set on GSE63885 dfs 0.499 (random median 0.525), q = 0.705; clinical label 0.530, q = 0.705.
- P3, P4 held: Gao set not distinguishable from random on any endpoint (LR AUC 0.49–0.54; all q = 0.705).
- P5 held for size 10 (0.500), missed narrowly for size 5 (0.498 vs predicted 0.50–0.58).
- P6 held: max published-set LR AUC 0.735 (≤ 0.75).

### Reading (wording for the supplement)
- Chen's 10 genes separate platinum-resistant from sensitive TCGA patients far better than random 10-gene sets (0.735, above A5's 500-gene ceiling of 0.634), yet are at chance on GSE63885 (0.499; random sets 0.525). This within-cohort-only pattern is what gene selection on overlapping patients produces; Chen et al. selected the genes on TCGA-OV patients with a PFI-based label using the full labelled set. Patient overlap cannot be verified (IDs not published), so state the pattern and the design fact, not a cause.
- Gao's 5 genes carry no signal distinguishable from random sets in TCGA or GSE63885 in this pipeline.
- Scope sentence (required): these results describe the gene lists as fixed inputs to this pipeline; they are not a reproduction of either study and do not address the performance those studies report.

# A8: BRCA1/2 germline + somatic; CCNE1

*Status:* pre-specified; deposited before running (d5bd844). *Script:* `label_validity/08_brca_germline.py`. *Summary:* `label_validity/outputs/08_brca_germline_summary.md`.

## Header (verbatim)

```text
label_validity/08_brca_germline.py
──────────────────────────────────
Q2 analysis A8 — BRCA1/2 known-groups test with germline + somatic variants, for every
label, including a direct same-patient comparison between label families.

Written 2026-10-29 ~19:30 ET, BEFORE the run. Prompted by the v3 peer review
(review_v3/PEER_REVIEW.md, major concern 1): A3 used somatic BRCA1/2 only (hrd/brca_status.csv,
PanCancer MAF), but the TCGA 2011 release (ov_tcga_pub data_mutations.txt) also carries
germline calls (Mutation_Status == "Germline": 51 BRCA1/2 rows).

DISCLOSURE — what was seen before these predictions were written
  * Count of germline/somatic BRCA rows in ov_tcga_pub (BRCA1 26 germline / 11 somatic; BRCA2 25 / 10;
    germline rows all truncating or splice).
  * One exploratory tabulation (main session, 2026-10-29 ~18:55 ET), carrier = any non-silent
    germline or somatic BRCA1/2, patients in ov_tcga_pub cases_sequenced, OS labels from the
    RNA-seq subset only (labels_master), sample OR / Fisher p:
      platinum 8/41 vs 53/145 (OR 0.42, p 0.058); pfiplat6 9/51 vs 63/175 (0.38, 0.016);
      os18 1/32 vs 11/98 (0.26, 0.29); os24 3/31 vs 19/95 (0.43, 0.28); response 5/55 vs 28/188 (0.57, 0.37).
    The reviewer reported the same tabulation.
  NOT seen: the truncating-only primary definition; OS labels in the full platinum cohort; the
  common-set comparison and bootstrap differences; BRCA1 vs BRCA2; CCNE1.
  Predictions P1–P3 are therefore informed by the exploratory tabulation; P4–P6 are not.

Population
  Platinum-treated patients (A1, n = 489) ∩ ov_tcga_pub case list `cases_sequenced` (316 tumours;
  patient = first 12 characters of the barcode).

Carrier definitions (BRCA1 or BRCA2; ov_tcga_pub data_mutations.txt)
  PRIMARY   germline or somatic truncating/splice variant: Variant_Classification in
            {Frame_Shift_Del, Frame_Shift_Ins, Nonsense_Mutation, Splice_Site}.
  SECONDARY (a) any non-silent germline or somatic (the exploratory definition);
            (b) germline only (truncating/splice); (c) BRCA1 only (primary rule);
            (d) BRCA2 only (primary rule); (e) somatic only, as in A3 (PanCancer hrd/brca_status.csv),
            restricted to the same sequenced patients, for comparison.
  Non-carriers: sequenced patients with no qualifying variant.

Labels (1 = non-responder / resistant)
  label_platinum, label_pfiplat6, label_response from labels_master.csv (A1).
  label_os18_all, label_os24_all: OS < 18 / 24 months, recomputed for ALL platinum-treated patients
  with src.preprocessing.extract_survival / assign_response_label (OS_MONTHS, OS_STATUS from
  ov_tcga_pan_can_atlas_2018; censored before the threshold → undetermined). A8 checks that these equal
  label_os18 / label_os24 wherever labels_master defines them (RNA-seq subset).

Tests (fixed before running)
  T1  Per label, all sequenced patients with the label determinate: 2×2 of carrier × label;
      conditional odds ratio with exact 95% CI (scipy odds_ratio, kind="conditional"); Fisher exact p.
  T2  COMMON SET: sequenced patients with label_platinum, label_os18_all and label_os24_all all determinate.
      Same OR per label in the common set. Difference in log OR, platinum − OS18 and platinum − OS24
      (and pfiplat6 − OS24 when pfiplat6 is also determinate in the common set), with 0.5 added to
      every cell (Haldane). 95% percentile CI from 2,000 bootstrap resamples of patients
      (numpy default_rng(42)).
  T3  BRCA1 vs BRCA2 separately (T1, platinum and pfiplat6 only).
  T4  CCNE1 amplification (GISTIC = 2 in ov_tcga_pub data_cna.txt; first CCNE1 row; patients in
      cases_cna ∩ platinum-treated) vs each label (T1 method). Secondary anchor: CCNE1 amplification
      is associated with primary platinum resistance (Etemadmoghadam 2009).

PREDICTIONS
  P1  label_platinum, primary carrier definition: OR < 1, 95% CI includes 1.
  P2  label_pfiplat6: OR < 1, 95% CI excludes 1.
  P3  label_os18_all and label_os24_all: OR < 1, 95% CI includes 1.
  P4  Common set: the bootstrap 95% CI of log OR(platinum) − log OR(OS24) includes 0, and likewise
      for OS18.
  P5  BRCA2 carriers have a lower OR than BRCA1 carriers for label_platinum (point estimates).
  P6  CCNE1 amplification: OR > 1 for label_platinum; 95% CI includes 1.

DECISION RULES (for the manuscript)
  * The primary BRCA definition in the manuscript becomes germline + somatic truncating/splice
    (this script). The A3 somatic-only result is reported as a secondary analysis.
  * If both T2 differences have 95% CIs that include 0, the manuscript does NOT claim that BRCA
    separates the platinum labels from the OS labels. BRCA is reported as associated with a
    favourable outcome under every label (convergent evidence), and the Results heading
    "Only the platinum labels show known-groups validity" is withdrawn.
  * If a difference CI excludes 0 with platinum more strongly associated (log-OR difference < 0),
    the discriminant claim is kept for that comparison and stated with the CI.
  * The A3 verdict labels ("BRCA-valid" etc.) are applied to T1 unchanged:
    "BRCA-valid" if OR < 1 and CI excludes 1; "direction only" if OR < 1 and CI includes 1;
    "not supported" if OR ≥ 1.

Inputs
  label_validity/outputs/labels_master.csv, hrd/brca_status.csv
  <data-root>/ov_tcga_pub/ov_tcga_pub/{data_mutations.txt, data_cna.txt,
      case_lists/cases_sequenced.txt, case_lists/cases_cna.txt}
  <data-root>/ov_tcga_pan_can_atlas_2018/{data_clinical_patient.txt, data_timeline_treatment.txt}
Outputs → label_validity/outputs/a8_brca_tests.csv, a8_brca_diff.csv, a8_carriers.csv,
          08_brca_germline_summary.md
Run (from the repo root; no model fitting, so the scikit-learn version does not matter):
  python label_validity/08_brca_germline.py --data-root "<...>/OV Data/Project data"
```

## Summary: results and scorecard (verbatim)

# A8 — BRCA1/2 germline + somatic known-groups test

Sequenced platinum-treated patients: 272; primary carriers: 55 (germline truncating 44); common set n = 180.

## T1 — each label, all determinate patients (carriers non-responding vs non-carriers)

**primary_trunc_germ_som**
- label_platinum: 7/37 vs 54/149; OR 0.41 [0.14, 1.04], p 0.051 — direction only
- label_pfiplat6: 8/47 vs 64/179; OR 0.37 [0.14, 0.87], p 0.014 — BRCA-valid
- label_response: 5/51 vs 28/192; OR 0.64 [0.18, 1.80], p 0.493 — direction only
- label_os18_all: 1/51 vs 23/195; OR 0.15 [0.00, 0.97], p 0.034 — BRCA-valid
- label_os24_all: 3/50 vs 43/192; OR 0.22 [0.04, 0.75], p 0.008 — BRCA-valid

**any_nonsilent_germ_som**
- label_platinum: 8/41 vs 53/145; OR 0.42 [0.16, 1.02], p 0.058 — direction only
- label_pfiplat6: 9/51 vs 63/175; OR 0.38 [0.15, 0.86], p 0.016 — BRCA-valid
- label_response: 5/55 vs 28/188; OR 0.57 [0.16, 1.61], p 0.371 — direction only
- label_os18_all: 1/55 vs 23/191; OR 0.14 [0.00, 0.88], p 0.021 — BRCA-valid
- label_os24_all: 3/54 vs 43/188; OR 0.20 [0.04, 0.67], p 0.003 — BRCA-valid

**germline_trunc**
- label_platinum: 7/29 vs 54/157; OR 0.61 [0.21, 1.59], p 0.389 — direction only
- label_pfiplat6: 8/38 vs 64/188; OR 0.52 [0.19, 1.24], p 0.131 — direction only
- label_response: 5/40 vs 28/203; OR 0.89 [0.25, 2.57], p 1.000 — direction only
- label_os18_all: 1/41 vs 23/205; OR 0.20 [0.00, 1.30], p 0.144 — direction only
- label_os24_all: 3/40 vs 43/202; OR 0.30 [0.06, 1.02], p 0.047 — direction only

**somatic_pancan_A3**
- label_platinum: 0/10 vs 40/117; OR 0.00 [0.00, 0.92], p 0.030 — BRCA-valid
- label_pfiplat6: 0/11 vs 49/147; OR 0.00 [0.00, 0.84], p 0.018 — BRCA-valid
- label_response: 2/13 vs 20/159; OR 1.26 [0.13, 6.45], p 0.674 — not supported
- label_os18_all: 0/12 vs 15/156; OR 0.00 [0.00, 3.80], p 0.604 — direction only
- label_os24_all: 0/12 vs 29/155; OR 0.00 [0.00, 1.68], p 0.129 — direction only

## T2 — common set (primary definition)

- label_platinum: 7/37 vs 52/143; OR 0.41 [0.14, 1.04], p 0.050 — direction only
- label_os18_all: 0/37 vs 12/143; OR 0.00 [0.00, 1.35], p 0.130 — direction only
- label_os24_all: 1/37 vs 28/143; OR 0.11 [0.00, 0.75], p 0.011 — BRCA-valid
- label_pfiplat6: 7/37 vs 52/140; OR 0.40 [0.14, 1.01], p 0.049 — direction only

Difference in log OR (Haldane), 2,000 bootstrap resamples:

- label_platinum − label_os18_all: +1.12 [-0.16, +2.00] (ratio of ORs 3.06; n 180, carriers 37); CI includes 0: True
- label_platinum − label_os24_all: +0.95 [-0.52, +2.71] (ratio of ORs 2.57; n 180, carriers 37); CI includes 0: True
- label_pfiplat6 − label_os24_all: +0.85 [-0.66, +2.56] (ratio of ORs 2.33; n 177, carriers 37); CI includes 0: True

## T3 — BRCA1 vs BRCA2 (primary rule)

- BRCA1_primary, label_platinum: 4/17 vs 57/169; OR 0.61 [0.14, 2.08], p 0.589 — direction only
- BRCA1_primary, label_pfiplat6: 4/25 vs 68/201; OR 0.37 [0.09, 1.17], p 0.109 — direction only
- BRCA2_primary, label_platinum: 3/21 vs 58/165; OR 0.31 [0.06, 1.12], p 0.082 — direction only
- BRCA2_primary, label_pfiplat6: 4/24 vs 68/202; OR 0.40 [0.09, 1.25], p 0.108 — direction only

## T4 — CCNE1 amplification

- label_platinum: 22/56 vs 65/221; OR 1.55 [0.80, 2.97], p 0.197
- label_pfiplat6: 28/70 vs 74/270; OR 1.76 [0.98, 3.15], p 0.056
- label_response: 13/80 vs 43/290; OR 1.11 [0.52, 2.26], p 0.727
- label_os18_all: 12/79 vs 26/285; OR 1.78 [0.78, 3.89], p 0.144
- label_os24_all: 22/78 vs 45/276; OR 2.01 [1.06, 3.75], p 0.022

## Prediction scorecard

Run 2026-10-29 ~19:30 ET in the cloud-linked VM (no model fitting), after the predictions were pushed to GitHub (commit d5bd844, 19:22 ET). One earlier dry run to a scratch folder outside the repo checked that the script runs; its output was not inspected.

Note: the A8 cohort is the sequenced patients who are also platinum-treated (272 of the 316 sequenced tumours). The header's exploratory tabulation was not restricted to platinum-treated patients in the same way and used OS labels from the RNA-seq subset only.

- **P1 — held.** label_platinum: OR 0.41 [0.14, 1.04] ("direction only").
- **P2 — held.** label_pfiplat6: OR 0.37 [0.14, 0.87] ("BRCA-valid").
- **P3 — FAILED.** OS labels in the full platinum cohort: OS18 OR 0.15 [0.00, 0.97]; OS24 OR 0.22 [0.04, 0.75]. Both CIs exclude 1, so BRCA is at least as strongly associated with the OS labels as with platinum status.
- **P4 — held.** Common set: log-OR difference platinum − OS18 +1.12 [−0.16, +2.00]; platinum − OS24 +0.95 [−0.52, +2.71]; pfiplat6 − OS24 +0.85 [−0.66, +2.56]. All CIs include 0, and the point estimates favour a STRONGER association with the OS labels.
- **P5 — held.** BRCA2 OR 0.31 vs BRCA1 OR 0.61 for label_platinum (point estimates; both CIs include 1).
- **P6 — held.** CCNE1 amplification, label_platinum: OR 1.55 [0.80, 2.97]. CCNE1 points the same way for every label (OS24 OR 2.01 [1.06, 3.75]).

Decision (pre-specified rule): BRCA does not separate the platinum labels from the OS labels. The manuscript withdraws "Only the platinum labels show known-groups validity" and reports BRCA (germline + somatic truncating, primary) and CCNE1 as associated in the expected direction under every label. A3's somatic-only result becomes a secondary analysis.

# A9: patients without a platinum status

*Status:* pre-specified; deposited before running (d5bd844). *Script:* `label_validity/09_platinum_missingness.py`. *Summary:* `label_validity/outputs/09_platinum_missingness_summary.md`.

## Header (verbatim)

```text
label_validity/09_platinum_missingness.py
─────────────────────────────────────────
Q2 analysis A9 — who lacks a determinate TCGA platinum status, and what the OS-threshold labels
capture.

Written 2026-10-29 ~19:40 ET, BEFORE the run. Prompted by the v3 peer review
(review_v3/PEER_REVIEW.md, major concerns 2–3): most early deaths appear to lack a platinum status,
so the primary label may be missing selectively among the patients most likely to be resistant.

DISCLOSURE — what was seen before these predictions were written
  * src_platinum_status_raw counts in the 489 platinum-treated patients: Sensitive 190, Resistant 87,
    Missing 87, Tooearly 57, absent from ov_tcga_pub 68.
  * In the RNA-seq OS cohorts (labels_master): of 22 patients with label_os18 = 1, 13 Missing,
    2 absent, 5 Resistant, 2 Sensitive; of 36 with label_os24 = 1, 16 Missing, 2 absent, 11 Resistant,
    7 Sensitive. Cross-tabs of label_os18/24 × label_platinum (PPV 5/7 and 11/18).
  * The 19 patients with a negative PFI-from-platinum interval: 10 Tooearly, 7 Resistant, 2 Missing.
  NOT seen: survival by status group; OS labels in the full cohort by status; pfiplat6, response,
  residual, stage or age by status group; the hybrid label; κmax/PABAK.
  Q2 and Q6 are therefore partly informed by the RNA-seq-subset counts above.

Populations
  PRIMARY: platinum-treated patients (A1, n = 489) present in the TCGA 2011 release (ov_tcga_pub),
    i.e. src_platinum_status_raw != "absent". Groups: DETERMINATE (Resistant, Sensitive) vs
    UNDETERMINED (Missing, Tooearly), with Missing and Tooearly also reported separately.
  SECONDARY: all 489, with "absent" added to UNDETERMINED.

Part A — comparison of DETERMINATE vs UNDETERMINED (primary population)
  A1  Overall survival (OS_MONTHS, OS_STATUS, PanCancer clinical): Kaplan–Meier median per group;
      two-sided log-rank test (chi-square, 1 df), implemented here.
  A2  Death before 18 and before 24 months (label_os18_all / label_os24_all as in A8: censored before
      the threshold excluded): proportion per group; Fisher exact OR (undetermined vs determinate).
  A3  Re-derived interval (label_pfiplat6, where determinate): proportion resistant per group; Fisher OR.
  A4  First-course response (label_response, PD/SD = 1): proportion per group; Fisher OR.
  A5  Descriptive only: suboptimal residual disease, stage IV, age (a3_covariates.csv); Fisher /
      Mann–Whitney p reported without a prediction.
Part B — what the OS-threshold labels capture (against label_platinum)
  In the RNA-seq subset (label_os18/24, as in A2) and in the full cohort (label_os18_all/24_all):
  sensitivity, specificity, PPV, NPV, LR+, Cohen's κ, maximum attainable κ given the marginals,
  and PABAK (2·p_o − 1).
Part C — descriptive: a "hybrid" platinum label = label_platinum where determinate, otherwise
  label_pfiplat6. Coverage and prevalence in the 489, and Part B metrics of OS labels against it.

PREDICTIONS
  Q1  UNDETERMINED patients have shorter OS than DETERMINATE: lower KM median and log-rank p < 0.05.
  Q2  Death before 18 months is more common in UNDETERMINED (Fisher OR > 1, p < 0.05).
  Q3  Among patients with label_pfiplat6 determinate, the resistant proportion is higher in UNDETERMINED
      (OR > 1).
  Q4  First-course PD/SD is more common in UNDETERMINED (OR > 1).
  Q6  Full cohort: PPV of label_os18_all and label_os24_all for platinum resistance ≥ 0.60, and
      sensitivity ≤ 0.30.

DECISION RULES (for the manuscript)
  * If Q1 holds and Q3 or Q4 holds: the manuscript states that TCGA platinum status is missing
    selectively among patients with poor outcomes ("valid but incomplete"). All agreement and
    sensitivity analyses of OS labels against platinum status are described as conditional on a
    determinate status, and the hybrid label is reported as a sensitivity analysis.
  * If Q1 fails: missingness is described as not associated with survival, and the framing does not
    rest on selective missingness.
  * Part B results replace the "OS labels miss most resistant patients" framing with the full set of
    sensitivity / PPV / LR+ / κmax, whatever they show.

Inputs
  label_validity/outputs/labels_master.csv, a3_covariates.csv
  <data-root>/ov_tcga_pan_can_atlas_2018/data_clinical_patient.txt
Outputs → label_validity/outputs/a9_group_tests.csv, a9_os_label_metrics.csv, a9_km.csv,
          09_platinum_missingness_summary.md
Run (from the repo root; no model fitting):
  python label_validity/09_platinum_missingness.py --data-root "<...>/OV Data/Project data"
```

## Summary: results and scorecard (verbatim)

# A9 — Who lacks a determinate platinum status; what OS labels capture

## Part A — primary_in_2011_release (undetermined vs determinate)

- A1 OS log-rank: n 144 vs 276; chi² 0.81, p 0.37
  - KM median OS, undetermined: 47.5 months (n 144, deaths 71)
  - KM median OS, determinate: 47.7 months (n 276, deaths 189)
- A2_death_lt18: 16/96 vs 22/268; OR 2.23 [1.04, 4.70], p 0.0307
- A2_death_lt24: 24/95 vs 43/259; OR 1.70 [0.92, 3.09], p 0.0684
- A3_pfiplat6_resistant: 13/68 vs 89/272; OR 0.49 [0.23, 0.96], p 0.0376
- A4_response_PDSD: 28/114 vs 28/255; OR 2.63 [1.41, 4.91], p 0.00147
- A5_residual_subopt: 37/127 vs 67/252; OR 1.13 [0.68, 1.87], p 0.627
- A5_stage_iv: 25/143 vs 41/277; OR 1.22 [0.68, 2.17], p 0.482
- A5 age: median difference -1.0 years, p 0.509

## Part A — secondary_all_489 (undetermined vs determinate)

- A1 OS log-rank: n 212 vs 276; chi² 0.05, p 0.83
  - KM median OS, undetermined: 48.8 months (n 212, deaths 93)
  - KM median OS, determinate: 47.7 months (n 276, deaths 189)
  - KM median OS, Missing: 39.0 months (n 87, deaths 61)
  - KM median OS, Tooearly: nan months (n 57, deaths 10)
  - KM median OS, Resistant: 32.9 months (n 87, deaths 77)
  - KM median OS, Sensitive: 58.2 months (n 189, deaths 112)
  - KM median OS, absent: 54.3 months (n 68, deaths 22)
- A2_death_lt18: 25/151 vs 22/268; OR 2.21 [1.15, 4.30], p 0.0148
- A2_death_lt24: 35/142 vs 43/259; OR 1.64 [0.96, 2.80], p 0.0644
- A3_pfiplat6_resistant: 26/117 vs 89/272; OR 0.59 [0.34, 0.99], p 0.0399
- A4_response_PDSD: 37/170 vs 28/255; OR 2.25 [1.28, 4.01], p 0.00363
- A5_residual_subopt: 37/127 vs 67/252; OR 1.13 [0.68, 1.87], p 0.627
- A5_stage_iv: 33/211 vs 41/277; OR 1.07 [0.63, 1.81], p 0.8
- A5 age: median difference +0.0 years, p 0.263

## Part B/C — OS labels against platinum status and the hybrid label

- os18_rnaseq vs platinum: n 139; sens 5/39 = 0.13; spec 0.98; PPV 5/7 = 0.71; NPV 0.74; LR+ 6.41; κ 0.144 (κmax 0.239); PABAK 0.482
- os24_rnaseq vs platinum: n 134; sens 11/39 = 0.28; spec 0.93; PPV 11/18 = 0.61; NPV 0.76; LR+ 3.83; κ 0.248 (κmax 0.549); PABAK 0.478
- os18_all vs platinum: n 268; sens 18/84 = 0.21; spec 0.98; PPV 18/22 = 0.82; NPV 0.73; LR+ 9.86; κ 0.241 (κmax 0.328); PABAK 0.478
- os24_all vs platinum: n 259; sens 32/83 = 0.39; spec 0.94; PPV 32/43 = 0.74; NPV 0.76; LR+ 6.17; κ 0.370 (κmax 0.594); PABAK 0.521
- os18_all vs hybrid: n 375; sens 29/108 = 0.27; spec 0.97; PPV 29/37 = 0.78; NPV 0.77; LR+ 8.96; κ 0.297 (κmax 0.426); PABAK 0.536
- os24_all vs hybrid: n 360; sens 47/107 = 0.44; spec 0.93; PPV 47/64 = 0.73; NPV 0.80; LR+ 6.54; κ 0.421 (κmax 0.677); PABAK 0.572

Hybrid label coverage: 394/489 (113 resistant / 281 sensitive); platinum status alone: 277/489.

## Prediction scorecard

Run 2026-10-29 ~19:30 ET (VM; no model fitting), after the predictions were pushed (commit d5bd844). One earlier dry run, output not inspected.

- **Q1 — FAILED.** No OS difference between undetermined and determinate (log-rank p 0.37; KM medians 47.5 vs 47.7 months). The undetermined group is heterogeneous: Missing has a median of 39.0 months (Resistant 32.9, Sensitive 58.2), while Tooearly has 10 deaths among 57 patients and the median is not reached.
- **Q2 — held.** Death before 18 months: 16/96 vs 22/268, OR 2.23 [1.04, 4.70].
- **Q3 — FAILED (opposite direction).** Resistant by re-derived interval: 13/68 vs 89/272, OR 0.49 [0.23, 0.96]. pfiplat6 is determinate for only 68 of 144 undetermined patients.
- **Q4 — held.** First-course PD/SD: 28/114 vs 28/255, OR 2.63 [1.41, 4.91].
- **Q6 — partly failed.** OS18 (full cohort): PPV 18/22 = 0.82, sensitivity 0.21 — held. OS24: PPV 32/43 = 0.74, but sensitivity 32/83 = 0.39 > 0.30 — failed.

Decision (pre-specified rule): Q1 failed, so the manuscript does NOT claim that platinum status is missing selectively among poor-outcome patients. Instead, it describes the undetermined group as heterogeneous: early deaths and first-course PD/SD are over-represented in it, but overall survival does not differ. Part B metrics replace the "OS labels miss most resistant patients" framing. In the full cohort, OS labels are specific (0.94–0.98) with high PPV (0.74–0.82) and LR+ 6–10, but insensitive (0.21–0.39). κ is bounded by κmax (OS18: 0.24 of a possible 0.33).

# A10: prognostic characteristics, full cohort

*Status:* pre-specified; deposited before running (e98b3d9). *Script:* `label_validity/10_prognostic_covariates.py`. *Summary:* `label_validity/outputs/10_prognostic_covariates_summary.md`.

## Header (verbatim)

```text
label_validity/10_prognostic_covariates.py
──────────────────────────────────────────
Q2 analysis A10 — do the OS-threshold labels track prognostic covariates (aneuploidy, residual
disease) differently from platinum status, in the FULL platinum-treated cohort and in the same patients?

Written 2026-10-29 ~19:35 ET, BEFORE the run. Prompted by A8/A9: A3 tested the OS labels only in the
RNA-seq subset (label_os18 / label_os24), while the platinum labels were tested in the full cohort.
The v3 claim "OS labels track aneuploidy and residual disease, platinum status does not" therefore
compared different patients.

DISCLOSURE — what was seen before these predictions were written
  * A3 results (a3_known_groups.csv): aneuploidy rank-biserial r: platinum +0.13 (q 0.21), pfiplat6
    +0.21, response −0.03, OS18 (RNA-seq) +0.42, OS24 (RNA-seq) +0.33. Suboptimal residual OR:
    platinum 1.12, pfiplat6 1.25, response 2.55, OS18 3.60 [1.16, 11.88], OS24 2.26 [0.93, 5.47].
    Stage IV: no label associated.
  * A8/A9 results (BRCA, CCNE1, OS label metrics, missingness).
  NOT seen: any covariate test with OS labels in the full cohort; any same-patient comparison.

Population and labels
  Platinum-treated patients (A1, n = 489). label_platinum, label_pfiplat6, label_response from
  labels_master.csv. label_os18_all / label_os24_all recomputed for all 489 exactly as in A8.
  Covariates from a3_covariates.csv (A3): aneuploidy, tmb, age, stage_iv, residual_subopt.

Tests (fixed before running)
  T1  Each label × covariate in all determinate patients: Fisher exact with conditional OR (binary
      covariates) or Mann–Whitney U with rank-biserial r (continuous; r > 0 = higher in label = 1).
      BH across the 5 covariates within each label.
  T2  COMMON SET: patients with label_platinum, label_os18_all and label_os24_all all determinate and
      the covariate non-missing. Per-label statistic in the common set. Then differences,
      OS18 − platinum and OS24 − platinum:
        aneuploidy: difference in rank-biserial r;
        residual_subopt: difference in log OR (Haldane 0.5).
      95% percentile CIs from 2,000 bootstrap resamples of patients (numpy default_rng(42)).

PREDICTIONS
  R1  Full cohort: aneuploidy r > 0 with BH q < 0.05 for label_os18_all and label_os24_all.
  R2  Full cohort: residual_subopt OR > 1 for label_os18_all and label_os24_all; 95% CI excludes 1 for
      label_os18_all.
  R3  Common set: point estimate of r(OS24) − r(platinum) for aneuploidy > 0, with 95% CI including 0.
  R4  Common set: point estimate of log OR(OS18) − log OR(platinum) for residual > 0, with 95% CI
      including 0.

DECISION RULES (for the manuscript)
  * If a T2 difference CI excludes 0 (OS label > platinum), the manuscript states that the OS label
    tracks that covariate more strongly than platinum status in the same patients, with the CI, as
    evidence that the OS labels carry prognostic content beyond platinum response.
  * If the T2 CIs include 0, the manuscript reports the per-label associations descriptively and does
    NOT claim that the OS labels track these covariates differently from platinum status.

Inputs: label_validity/outputs/labels_master.csv, a3_covariates.csv;
        <data-root>/ov_tcga_pan_can_atlas_2018/data_clinical_patient.txt
Outputs → label_validity/outputs/a10_tests.csv, a10_diff.csv, 10_prognostic_covariates_summary.md
Run (from the repo root; no model fitting):
  python label_validity/10_prognostic_covariates.py --data-root "<...>/OV Data/Project data"
```

## Summary: results and scorecard (verbatim)

# A10 — Prognostic covariates by label, full cohort and same patients

Common set (platinum, OS18_all, OS24_all determinate): n = 259.

## T1 — all determinate patients (BH across 5 covariates within label)

**label_platinum**
- residual_subopt: OR +1.116 [0.59, 2.09]; n 252; p 0.762; q 0.952
- stage_iv: OR +1.016 [0.46, 2.17]; n 277; p 1; q 1
- aneuploidy: rank_biserial_r +0.125; n 265; p 0.103; q 0.258
- tmb: rank_biserial_r -0.157; n 255; p 0.0432; q 0.216
- age: rank_biserial_r +0.072; n 277; p 0.337; q 0.562

**label_pfiplat6**
- residual_subopt: OR +1.251 [0.71, 2.18]; n 310; p 0.415; q 0.518
- stage_iv: OR +1.088 [0.57, 2.03]; n 388; p 0.762; q 0.762
- aneuploidy: rank_biserial_r +0.211; n 373; p 0.00133; q 0.00665
- tmb: rank_biserial_r -0.057; n 354; p 0.397; q 0.518
- age: rank_biserial_r +0.146; n 389; p 0.0229; q 0.0572

**label_response**
- residual_subopt: OR +2.549 [1.31, 4.91]; n 335; p 0.0035; q 0.0175
- stage_iv: OR +1.251 [0.57, 2.57]; n 424; p 0.579; q 0.72
- aneuploidy: rank_biserial_r -0.031; n 409; p 0.696; q 0.72
- tmb: rank_biserial_r -0.028; n 391; p 0.72; q 0.72
- age: rank_biserial_r +0.060; n 425; p 0.441; q 0.72

**label_os18_all**
- residual_subopt: OR +2.858 [1.30, 6.29]; n 328; p 0.00473; q 0.0118
- stage_iv: OR +1.753 [0.76, 3.79]; n 418; p 0.138; q 0.173
- aneuploidy: rank_biserial_r +0.205; n 404; p 0.0223; q 0.0372
- tmb: rank_biserial_r -0.075; n 379; p 0.419; q 0.419
- age: rank_biserial_r +0.261; n 419; p 0.00348; q 0.0118

**label_os24_all**
- residual_subopt: OR +2.410 [1.28, 4.50]; n 318; p 0.0038; q 0.00633
- stage_iv: OR +1.551 [0.78, 2.97]; n 400; p 0.175; q 0.218
- aneuploidy: rank_biserial_r +0.253; n 386; p 0.000586; q 0.00147
- tmb: rank_biserial_r -0.078; n 361; p 0.309; q 0.309
- age: rank_biserial_r +0.277; n 401; p 0.000145; q 0.000727

## T2 — common set

- label_platinum × aneuploidy: rank_biserial_r +0.114; n 248; p 0.151
- label_platinum × residual_subopt: OR +1.137 [0.59, 2.18]; n 236; p 0.754
- label_os18_all × aneuploidy: rank_biserial_r +0.057; n 248; p 0.663
- label_os18_all × residual_subopt: OR +1.612 [0.52, 4.62]; n 236; p 0.422
- label_os24_all × aneuploidy: rank_biserial_r +0.221; n 248; p 0.0226
- label_os24_all × residual_subopt: OR +1.869 [0.82, 4.12]; n 236; p 0.106

Differences (2,000 bootstrap resamples):

- aneuploidy, label_os18_all − label_platinum: Δ rank-biserial r -0.057 [-0.347, +0.206] (n 248); CI includes 0: True
- aneuploidy, label_os24_all − label_platinum: Δ rank-biserial r +0.107 [-0.094, +0.305] (n 248); CI includes 0: True
- residual_subopt, label_os18_all − label_platinum: Δ log OR (Haldane) +0.370 [-0.663, +1.253] (n 236); CI includes 0: True
- residual_subopt, label_os24_all − label_platinum: Δ log OR (Haldane) +0.501 [-0.232, +1.209] (n 236); CI includes 0: True

## Prediction scorecard

Run 2026-10-29 ~19:32 ET (VM; no model fitting), after the predictions were pushed (commit e98b3d9). One earlier dry run, output not inspected.

- **R1 — held.** Aneuploidy, full cohort: OS18_all r +0.205 (q 0.037); OS24_all r +0.253 (q 0.0015).
- **R2 — held.** Residual disease, full cohort: OS18_all OR 2.86 [1.30, 6.29]; OS24_all OR 2.41 [1.28, 4.50].
- **R3 — held.** Common set (n 248): Δr aneuploidy, OS24 − platinum +0.107 [−0.094, +0.305]. Also OS18 − platinum −0.057 [−0.347, +0.206].
- **R4 — held.** Common set (n 236): Δ log OR residual, OS18 − platinum +0.37 [−0.66, +1.25]. Also OS24 − platinum +0.50 [−0.23, +1.21].

Decision (pre-specified rule): all four difference CIs include 0. The manuscript reports the per-label associations descriptively and does NOT claim that the OS labels track aneuploidy or residual disease differently from platinum status. The v3 sentence "the OS labels instead tracked aneuploidy and residual disease" is withdrawn as a contrast between labels.

Not pre-specified (observation only): age is associated with both OS labels in the full cohort (r +0.26, +0.28; q ≤ 0.012) but not with platinum status (r +0.07, q 0.56). No same-patient difference test was run for age, so this is reported, if at all, as an observation.

# A11: full-cohort label table, agreement, OS-as-test

*Status:* descriptive; no predictions. *Script:* `label_validity/11_full_cohort_labels.py`. *Summary:* `label_validity/outputs/11_full_cohort_labels_summary.md`.

## Header (verbatim)

```text
label_validity/11_full_cohort_labels.py
───────────────────────────────────────
A11 — descriptive extension of A1/A2 to the full platinum-treated cohort (no new predictions).

Why: A8–A10 showed that the OS-threshold labels must be compared with the platinum labels in the
same, full cohort (489 platinum-treated patients), not only in the RNA-seq subset used by A2. This
script derives no new kind of result. It (1) writes the per-patient label table used by the
reframed manuscript and its figures, and (2) recomputes A2's agreement and sensitivity/specificity
with the full-cohort OS labels, using A2's code and settings unchanged (κ with 2,000-resample
percentile bootstrap, seed 42; Wilson 95% intervals). It adds PPV/NPV with Wilson intervals.
Written 2026-10-29 ~20:00 ET after A8–A10 had been run; A9 had already reported point estimates
of the same sensitivity/specificity/PPV.

Labels (1 = non-responder / resistant)
  label_platinum, label_pfiplat6, label_response   from labels_master.csv (A1)
  label_os18_all, label_os24_all                   OS < 18 / 24 months for all platinum-treated patients,
                                                   recomputed with src.preprocessing exactly as in A8–A10
  label_hybrid                                     label_platinum where determinate, else label_pfiplat6 (A9 Part C)

Outputs → label_validity/outputs/labels_full.csv, a11_coverage.csv, a11_kappa_full.csv,
          a11_os_test_full.csv, 11_full_cohort_labels_summary.md
Run (from the repo root; no model fitting):
  python label_validity/11_full_cohort_labels.py --data-root "<...>/OV Data/Project data"
```

## Summary: results and scorecard (verbatim)

# A11 — Full-cohort label table, coverage, agreement and OS-as-test (descriptive)

## Coverage (of 489 platinum-treated patients)

- label_platinum: 277 determinate (87 non-responder / 190 responder); 145 with RNA-seq
- label_pfiplat6: 389 determinate (115 non-responder / 274 responder); 188 with RNA-seq
- label_response: 425 determinate (65 non-responder / 360 responder); 219 with RNA-seq
- label_os18_all: 419 determinate (47 non-responder / 372 responder); 206 with RNA-seq
- label_os24_all: 401 determinate (78 non-responder / 323 responder); 199 with RNA-seq
- label_hybrid: 394 determinate (113 non-responder / 281 responder); 189 with RNA-seq

## Cohen's κ (full cohort; 2,000-resample bootstrap, seed 42)

- label_platinum × label_pfiplat6: κ 0.966 [0.930, 0.992], agreement 0.985, n 272
- label_platinum × label_response: κ 0.257 [0.137, 0.380], agreement 0.741, n 255
- label_platinum × label_os18_all: κ 0.241 [0.138, 0.350], agreement 0.739, n 268
- label_platinum × label_os24_all: κ 0.370 [0.248, 0.486], agreement 0.761, n 259
- label_pfiplat6 × label_response: κ 0.213 [0.105, 0.321], agreement 0.728, n 353
- label_pfiplat6 × label_os18_all: κ 0.314 [0.212, 0.413], agreement 0.771, n 371
- label_pfiplat6 × label_os24_all: κ 0.441 [0.340, 0.545], agreement 0.792, n 356
- label_response × label_os18_all: κ 0.259 [0.127, 0.391], agreement 0.838, n 371
- label_response × label_os24_all: κ 0.250 [0.123, 0.370], agreement 0.793, n 358
- label_os18_all × label_os24_all: κ 0.710 [0.608, 0.797], agreement 0.923, n 401

## OS labels as a test for platinum resistance (Wilson 95% CI)

- label_os18_all vs label_platinum (n 268): sensitivity 18/84 = 0.21 [0.14, 0.31]; specificity 180/184 = 0.98 [0.95, 0.99]; PPV 18/22 = 0.82 [0.61, 0.93]; NPV 0.73 [0.67, 0.78]
- label_os24_all vs label_platinum (n 259): sensitivity 32/83 = 0.39 [0.29, 0.49]; specificity 165/176 = 0.94 [0.89, 0.96]; PPV 32/43 = 0.74 [0.60, 0.85]; NPV 0.76 [0.70, 0.82]
- label_os18_all vs label_hybrid (n 375): sensitivity 29/108 = 0.27 [0.19, 0.36]; specificity 259/267 = 0.97 [0.94, 0.98]; PPV 29/37 = 0.78 [0.63, 0.89]; NPV 0.77 [0.72, 0.81]
- label_os24_all vs label_hybrid (n 360): sensitivity 47/107 = 0.44 [0.35, 0.53]; specificity 236/253 = 0.93 [0.90, 0.96]; PPV 47/64 = 0.73 [0.62, 0.83]; NPV 0.80 [0.75, 0.84]

# A12: approximate AUC intervals

*Status:* descriptive; no predictions. *Script:* `label_validity/12_auc_intervals.py`.

## Header (verbatim)

```text
label_validity/12_auc_intervals.py
──────────────────────────────────
A12 — descriptive: approximate 95% intervals for the within-TCGA cross-validated AUCs of A5
(no refitting). Added 2026-10-29 in response to the v3 reviews (no CI on within-TCGA AUCs).

For each train → test cell of a5_cross_label_repeats.csv: mean AUC over 3 models × 5 repeats,
the range over those 15 values, and a Hanley–McNeil (1982) normal-approximation 95% interval for
the mean AUC, using the cell's numbers of positive and negative patients. The Hanley–McNeil interval
treats the mean AUC as one AUC from n_pos and n_neg patients; it ignores between-repeat and
between-model variation and is reported only as an indication of precision.
Output → label_validity/outputs/a12_auc_intervals.csv
Run: python label_validity/12_auc_intervals.py
```

# A13: exploratory label structure

*Status:* exploratory, post hoc; no predictions. *Script:* `label_validity/13_exploratory_label_structure.py`. *Summary:* `label_validity/outputs/13_exploratory_label_structure_summary.md`.

## Header (verbatim)

```text
label_validity/13_exploratory_label_structure.py
────────────────────────────────────────────────
A13 — EXPLORATORY, POST HOC. Written 2026-10-29 ~21:00 ET AFTER the v4 red-team review
(review_v4/METHODS_ATTACK.md, CODE_ATTACK.md), whose scratch analyses had already shown most of these
results (review_v4/scratch_methods/). There are no predictions and no decision rules: every quantity
below is reported whatever it shows, and the manuscript labels it exploratory.

Purpose: answer the reviewers' questions about what the OS-threshold labels measure, re-implementing
the red-team analyses as one documented script that reads only committed inputs.
  E1  Cohort flow: TCGA-OV patients in the PanCancer clinical file → treatment record → platinum agent.
  E2  Threshold sweep: OS < t months (t = 6 … 60) as a test for platinum resistance (reference:
      platinum status; and the combined label). n, sensitivity, specificity, PPV, NPV (Wilson 95% CI),
      κ, κmax, Youden, plus the values expected with NO platinum information (independence:
      PPV = prevalence of resistance; specificity = 1 − P(OS label positive)) and the maximum
      sensitivity the label's prevalence allows.
  E3  Reference missingness: among OS-positive patients, how many lack a determinate platinum status,
      and best/worst-case bounds on sensitivity and PPV if all of them were resistant / sensitive.
  E4  Decomposition of OS into PFI-from-platinum and survival after progression (Cox, lifelines):
      age (per 10 y), stage IV, residual > 1 cm, any residual, BRCA1/2 carrier (A8 primary),
      CCNE1 amplification, Aneuploidy Score (per SD). Times from TCGA-CDR (days).
  E5  Clinical-only classifier: 5 × 5-fold stratified CV logistic regression (age, stage IV,
      residual > 1 cm; complete cases; seed 42) predicting each label; mean AUC (pooled out-of-fold per repeat).
  E6  Residual disease coded as any residual vs none (R0): Fisher conditional OR for each label.
  E7  Minimum detectable differences for the same-patient comparisons in A8/A10: 80% power, two-sided
      α 0.05, SE taken from the bootstrap 95% CI width (SE ≈ width / 3.92); MDE = 2.80 × SE.
  E8  Sensitivity: excluding the TCGA-CDR "Redacted" patients from the re-derived interval —
      coverage and κ with platinum status.

Inputs: label_validity/outputs/{labels_full.csv, labels_master.csv, a3_covariates.csv, a8_carriers.csv,
        a8_brca_diff.csv, a10_diff.csv}; <data-root>/ov_tcga_pan_can_atlas_2018/{data_clinical_patient.txt,
        data_timeline_treatment.txt}; <data-root>/ov_tcga_pub/ov_tcga_pub/{data_clinical_sample.txt,
        data_cna.txt, case_lists/cases_cna.txt}; <data-root>/TCGA-CDR-SupplementalTableS1.xlsx
Outputs → label_validity/outputs/a13_*.csv, 13_exploratory_label_structure_summary.md
Run (from the repo root): python label_validity/13_exploratory_label_structure.py --data-root "<...>/OV Data/Project data"
Requires lifelines for E4.
```

## Summary: results and scorecard (verbatim)

# A13 — Exploratory analyses of label structure (post hoc; no predictions)

## E1 Cohort flow

- PanCancer clinical patients: 585
- with any treatment-timeline record: 496
- no treatment-timeline record (excluded): 89; KM median OS 27.6 mo; determinate platinum status 5
- treatment record but no carboplatin/cisplatin (excluded): 7; KM median OS 51.4 mo; determinate platinum status 2
- platinum-treated cohort: 489; KM median OS 47.7 mo; determinate platinum status 277

## E2 Threshold sweep (reference: platinum status)

| t (mo) | n | sens [95% CI] | spec | PPV [95% CI] | κ (κmax) | Youden | PPV if no platinum information | spec if no platinum information | max sens allowed |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 276 | 0.02 [0.01, 0.08] | 1.00 | 1.00 [0.34, 1.00] | 0.03 (0.03) | 0.02 | 0.32 | 0.99 | 0.02 |
| 9 | 274 | 0.05 [0.02, 0.11] | 1.00 | 1.00 [0.51, 1.00] | 0.06 (0.06) | 0.05 | 0.31 | 0.99 | 0.05 |
| 12 | 274 | 0.10 [0.06, 0.19] | 1.00 | 1.00 [0.70, 1.00] | 0.14 (0.14) | 0.10 | 0.31 | 0.97 | 0.10 |
| 15 | 271 | 0.14 [0.08, 0.23] | 0.98 | 0.80 [0.55, 0.93] | 0.16 (0.23) | 0.13 | 0.31 | 0.94 | 0.18 |
| 18 | 268 | 0.21 [0.14, 0.31] | 0.98 | 0.82 [0.61, 0.93] | 0.24 (0.33) | 0.19 | 0.31 | 0.92 | 0.26 |
| 21 | 265 | 0.35 [0.25, 0.45] | 0.96 | 0.81 [0.65, 0.90] | 0.36 (0.51) | 0.31 | 0.32 | 0.86 | 0.43 |
| 24 | 259 | 0.39 [0.29, 0.49] | 0.94 | 0.74 [0.60, 0.85] | 0.37 (0.59) | 0.32 | 0.32 | 0.83 | 0.52 |
| 30 | 249 | 0.46 [0.36, 0.57] | 0.88 | 0.66 [0.53, 0.76] | 0.37 (0.76) | 0.34 | 0.33 | 0.77 | 0.71 |
| 36 | 243 | 0.64 [0.53, 0.74] | 0.83 | 0.65 [0.54, 0.75] | 0.47 (0.99) | 0.47 | 0.33 | 0.67 | 0.99 |
| 42 | 238 | 0.74 [0.64, 0.82] | 0.72 | 0.58 [0.48, 0.67] | 0.43 (0.80) | 0.46 | 0.34 | 0.56 | 1.00 |
| 48 | 233 | 0.85 [0.76, 0.91] | 0.63 | 0.54 [0.46, 0.63] | 0.42 (0.62) | 0.48 | 0.34 | 0.46 | 1.00 |
| 60 | 226 | 0.95 [0.88, 0.98] | 0.46 | 0.48 [0.41, 0.56] | 0.33 (0.40) | 0.41 | 0.35 | 0.31 | 1.00 |

## E3 OS-positive patients without a platinum status; bounds

- OS < 18 mo: 47 positive, of whom 25 undetermined (53%); PPV observed 0.82, bounds 0.38–0.91; sensitivity observed 0.21, bounds 0.09–0.39 (lower: undetermined OS-negative all resistant; upper: undetermined OS-positive all resistant)
- OS < 24 mo: 78 positive, of whom 35 undetermined (45%); PPV observed 0.74, bounds 0.41–0.86; sensitivity observed 0.39, bounds 0.17–0.57 (lower: undetermined OS-negative all resistant; upper: undetermined OS-positive all resistant)

## E4 Cox decomposition (HR [95% CI], p; n/events)

| covariate | PFI from platinum | survival after progression | OS |
|---|---|---|---|
| age10 | 1.08 [0.98, 1.19], p 0.114 (436/328) | 1.26 [1.12, 1.42], p 0.000174 (331/237) | 1.22 [1.10, 1.36], p 0.000241 (488/282) |
| stage_iv | 1.28 [0.96, 1.71], p 0.0904 (435/327) | 1.03 [0.74, 1.43], p 0.863 (331/237) | 1.30 [0.96, 1.74], p 0.085 (487/281) |
| residual_subopt | 1.11 [0.85, 1.44], p 0.45 (349/273) | 1.41 [1.03, 1.93], p 0.0311 (267/202) | 1.48 [1.12, 1.96], p 0.00532 (378/240) |
| resid_any | 1.67 [1.23, 2.26], p 0.000953 (349/273) | 1.66 [1.11, 2.48], p 0.0131 (267/202) | 2.21 [1.52, 3.21], p 3.07e-05 (378/240) |
| brca_carrier | 0.55 [0.38, 0.79], p 0.00132 (247/202) | 0.68 [0.44, 1.06], p 0.0904 (201/152) | 0.50 [0.34, 0.75], p 0.000778 (271/178) |
| ccne1_amp | 1.56 [1.19, 2.06], p 0.00143 (384/297) | 1.18 [0.86, 1.63], p 0.297 (294/218) | 1.46 [1.09, 1.95], p 0.0111 (421/260) |
| aneuploidy_sd | 1.20 [1.07, 1.35], p 0.00131 (418/313) | 1.03 [0.90, 1.17], p 0.706 (317/225) | 1.17 [1.04, 1.32], p 0.0109 (470/270) |

## E5 Clinical-only logistic regression (age, stage IV, residual > 1 cm), 5×5 CV

- label_platinum: AUC 0.479 (range 0.469–0.493); n 252 (82 positive)
- label_pfiplat6: AUC 0.517 (range 0.503–0.530); n 309 (96 positive)
- label_hybrid: AUC 0.487 (range 0.478–0.498); n 314 (95 positive)
- label_response: AUC 0.542 (range 0.510–0.561); n 334 (52 positive)
- label_os18_all: AUC 0.641 (range 0.620–0.653); n 327 (34 positive)
- label_os24_all: AUC 0.622 (range 0.607–0.632); n 317 (60 positive)

## E6 Any residual vs none (R0)

- label_platinum: 74/200 vs 8/52; OR 3.22 [1.40, 8.35], p 0.00269
- label_pfiplat6: 86/244 vs 10/66; OR 3.04 [1.44, 7.03], p 0.00152
- label_hybrid: 85/248 vs 10/67; OR 2.96 [1.41, 6.85], p 0.00246
- label_response: 44/265 vs 8/70; OR 1.54 [0.67, 3.99], p 0.355
- label_os18_all: 31/260 vs 3/68; OR 2.93 [0.87, 15.43], p 0.0763
- label_os24_all: 54/251 vs 6/67; OR 2.78 [1.12, 8.29], p 0.0216

## E7 Minimum detectable difference (80% power) for same-patient comparisons

- BRCA log OR: label_platinum − label_os18_all: estimate +1.12, SE 0.55, MDE 1.54 (ratio of ORs 4.7)
- BRCA log OR: label_platinum − label_os24_all: estimate +0.95, SE 0.82, MDE 2.31 (ratio of ORs 10.0)
- BRCA log OR: label_pfiplat6 − label_os24_all: estimate +0.85, SE 0.82, MDE 2.30 (ratio of ORs 10.0)
- Δ rank-biserial r: label_os18_all − label_platinum: estimate -0.06, SE 0.14, MDE 0.40
- Δ rank-biserial r: label_os24_all − label_platinum: estimate +0.11, SE 0.10, MDE 0.28
- Δ log OR (Haldane): label_os18_all − label_platinum: estimate +0.37, SE 0.49, MDE 1.37 (ratio of ORs 3.9)
- Δ log OR (Haldane): label_os24_all − label_platinum: estimate +0.50, SE 0.37, MDE 1.03 (ratio of ORs 2.8)

## E8 Excluding TCGA-CDR 'Redacted' patients from the re-derived interval

- Redacted among platinum-treated: 38; re-derived interval determinate 389 → 358 (108 resistant); κ with platinum status 0.964 (n 251)

# A14: cohort characteristics

*Status:* descriptive; no predictions. *Script:* `label_validity/14_cohort_characteristics.py`.

## Header (verbatim)

```text
label_validity/14_cohort_characteristics.py
───────────────────────────────────────────
A14 — descriptive (no predictions): baseline characteristics of the 489 platinum-treated patients and of the
251 with RNA-seq data, for the reporting checklist (STROBE item 14 / STARD item 20). Added 2026-10-29.
Inputs: label_validity/outputs/labels_full.csv, a3_covariates.csv, a8_carriers.csv; ov_tcga_pub case list (sequenced).
Output → label_validity/outputs/a14_cohort_characteristics.csv
Run: python label_validity/14_cohort_characteristics.py --data-root "<...>/OV Data/Project data"
```

# A15: provenance audit of the re-derived interval

*Status:* pre-specified after external review; deposited before running (d349b2b). *Script:* `label_validity/15_reconstruction_provenance.py`. *Summary:* `label_validity/outputs/15_reconstruction_provenance_summary.md`.

## Header (verbatim)

```text
label_validity/15_reconstruction_provenance.py
──────────────────────────────────────────────
A15 — patient-level provenance audit of the re-derived platinum-free-interval label (label_pfiplat6),
especially in the patients it ADDS to TCGA's published platinum status, and a "strict" combined label.

Written 2026-10-29 ~22:15 ET, BEFORE the run, in response to an external review of manuscript v5 (point 2:
"agreement in the overlap does not establish accuracy in the additional 117 patients … audit the added
cases, the four disagreements, ambiguous treatment courses, and event types"; TCGA-CDR's progression-free
interval counts new tumour events and death with tumour).

DISCLOSURE — seen before writing: the label counts (labels_full.csv: 394 combined, 117 added, 4 disagreements,
8 negative intervals classed resistant, 11 undetermined); that 38 platinum-treated patients have a redacted
TCGA-CDR record (A13); that 6 resistant calls are deaths with tumour (red-team code audit, m2); the CDR column
values (new_tumor_event_type: Recurrence 294, Progression of Disease 34). Not seen: any per-patient provenance
class, the flags below, or any result with the strict label.

Population: the 489 platinum-treated patients; focus on patients with label_pfiplat6 determinate.
For each such patient (sources: TCGA-CDR; PanCanAtlas treatment timeline):
  event_source (resistant calls): "recorded_new_tumour_event" if new_tumor_event_dx_days_to equals PFI.time
      (± 1 day) — with its type (Recurrence / Progression of Disease); "death_counted_as_progression" if there is
      no matching new tumour event and death_days_to equals PFI.time (± 1 day); otherwise "unclear".
  negative_interval: PFI.time before the end of first-line platinum.
  flags: redacted CDR record; an adjuvant platinum row with a missing STOP_DATE (stop date taken from other rows);
      a later-line treatment (REGIMEN_INDICATION Progression / Recurrence) STARTED before the recorded PFI event
      (or, for sensitive patients, before day 183 after the end of platinum), which suggests that progression was
      recorded late; interval within 150–215 days (near the 183-day cut-off).
  provenance_class: "clean_resistant" (recorded new tumour event after the end of platinum, no flag);
      "clean_sensitive" (interval ≥ 183 days, no flag); "flagged" (any flag, a death-only event or an unclear event);
      "negative_interval" (progression recorded before the end of platinum; reported separately).
Strict combined label: TCGA platinum status where determinate; otherwise label_pfiplat6 only for
      clean_resistant / clean_sensitive patients.

PREDICTIONS
  P1  ≥ 75% of the resistant calls among the ADDED patients are backed by a recorded new tumour event
      (not death-only or unclear).
  P2  The strict combined label covers ≥ 370 of the 489 patients.
  P3  Against the strict combined label, sensitivity and PPV of the 18- and 24-month OS thresholds are each
      within 0.05 of their values against the broad combined label (sensitivity 0.27 / 0.44; PPV 0.78 / 0.73).
  P4  At least 2 of the 4 disagreements between platinum status and the re-derived interval carry a flag or
      an interval within 150–215 days.

DECISION RULES (for the manuscript)
  * The manuscript reports the provenance classes of the added patients and of the 4 disagreements.
  * If P1 fails, or if more than 20% of the added patients are not clean, the manuscript recommends the
    STRICT combined label and reports the broad one as a sensitivity analysis; otherwise it reports both,
    recommending the broad label with the provenance table.
  * Whatever the result, the per-patient provenance table is released with the label resource.

Run (from the repo root; no model fitting): python label_validity/15_reconstruction_provenance.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a15_provenance.csv (per patient), a15_class_by_group.csv, a15_resistant_event_source.csv,
          a15_os_test_strict.csv, a15_label_combined_strict.csv, 15_reconstruction_provenance_summary.md
```

## Summary: results and scorecard (verbatim)

# A15 — Provenance of the re-derived platinum-free-interval label

Re-derived interval determinate: 389; overlap with platinum status: 272; added by reconstruction: 117 (26 resistant).

## Provenance class by group and label

```
provenance_class                             clean_resistant  clean_sensitive  flagged  negative_interval  All
group                        label_pfiplat6                                                                   
added_by_reconstruction      0.0                           0               73       18                  0   91
                             1.0                          17                0        8                  1   26
overlap_with_platinum_status 0.0                           0              160       23                  0  183
                             1.0                          75                0        7                  7   89
All                                                       92              233       56                  8  389
```

## Event source of resistant calls

```
event_source                  death_counted_as_progression  recorded_new_tumour_event:Progression of Disease  recorded_new_tumour_event:Recurrence  recorded_new_tumour_event:nan  All
group                                                                                                                                                                                 
added_by_reconstruction                                  6                                                 3                                    13                              4   26
overlap_with_platinum_status                             0                                                12                                    77                              0   89
All                                                      6                                                15                                    90                              4  115
```

Added resistant calls backed by a recorded new tumour event: 20/26.
Added patients classed clean: 90/117.
Strict combined label: 367 determinate (104 resistant / 263 sensitive).

## The disagreements between platinum status and the re-derived interval

```
                                     group  label_platinum  label_pfiplat6  pfi_from_platinum_d                          event_source provenance_class  redacted  adj_platinum_rows  adj_platinum_stop_missing  later_line_before_event  near_threshold  disagreement src_platinum_status_raw
PATIENT_ID                                                                                                                                                                                                                                                                                   
TCGA-24-2029  overlap_with_platinum_status             0.0             1.0                154.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False            True          True               Sensitive
TCGA-29-1774  overlap_with_platinum_status             0.0             1.0                101.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  3                      False                    False           False          True               Sensitive
TCGA-61-2009  overlap_with_platinum_status             0.0             1.0                 18.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
TCGA-61-2113  overlap_with_platinum_status             0.0             1.0                148.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
```

## OS thresholds as tests: broad vs strict combined reference

- label_os18_all vs label_hybrid (n 375): sensitivity 29/108 = 0.27 [0.19, 0.36]; PPV 29/37 = 0.78 [0.63, 0.89]
- label_os24_all vs label_hybrid (n 360): sensitivity 47/107 = 0.44 [0.35, 0.53]; PPV 47/64 = 0.73 [0.62, 0.83]
- label_os18_all vs label_combined_strict (n 349): sensitivity 24/99 = 0.24 [0.17, 0.34]; PPV 24/30 = 0.80 [0.63, 0.90]
- label_os24_all vs label_combined_strict (n 335): sensitivity 40/98 = 0.41 [0.32, 0.51]; PPV 40/53 = 0.75 [0.62, 0.85]

## Prediction scorecard

~~(to be completed after the run)~~

Run 2026-10-29 ~22:00 ET in the cloud-linked VM (no model fitting), after the script with its predictions and decision rules was committed (d349b2b, 21:56:39 ET; now on GitHub main). All outputs have modification time 22:00:17 ET. The script does not record package versions; the VM's current interpreter is Python 3.10.12, pandas 2.3.3, numpy 2.2.6 (checked ~22:15 ET, after the run).

Correction to the script header: it says "Written 2026-10-29 ~22:15 ET, BEFORE the run". That time was a wrong estimate. The script was committed at 21:56:39 ET (d349b2b), so it was written before then. The commit timestamp is authoritative, and the run followed it.

Deviation (found when filling this scorecard): the header lists "interval within 150–215 days (near the 183-day cut-off)" among the flags, and defines "clean" as "no flag". The code (line 114) builds `any_flag` from the redacted record, the missing adjuvant stop date and the later-line flag only; `near_threshold` is computed but does not enter `provenance_class`. As implemented, 12 added patients with an interval of 150–215 days (5 resistant, 7 sensitive) are classed clean and enter the strict label. Under the header's definition:
- added patients not clean would be 39/117 (33%) instead of 27/117 (23%);
- the strict combined label would cover 355 patients (99 resistant / 256 sensitive) instead of 367 (104 / 263).
P1 and P4 do not depend on this (P4 counts flags and near-threshold intervals separately). P2 fails under either definition. The decision rule outcome is the same under either definition.

Resolution (Aaron, 2026-10-29, before the 15b run): the manuscript follows the header's definition. `15b_reconstruction_provenance_specfix.py` is this script with near_threshold added to any_flag and nothing else changed; it was run at 22:25 ET (outputs `a15b_*`, `15b_reconstruction_provenance_specfix_summary.md`). It gives 78/117 added patients clean and a strict combined label of 355 (99 resistant / 256 sensitive). Against that label, OS18 sensitivity is 0.23 [0.16, 0.33] and PPV 0.79 [0.60, 0.90]; OS24 sensitivity 0.41 [0.31, 0.51] and PPV 0.75 [0.61, 0.84]. These are still within 0.05 of the broad-label values, so P3 holds under either definition. The as-run label (367) is kept unchanged as `a15_label_combined_strict.csv`.

- **P1 — held (narrowly).** 20/26 resistant calls among the added patients (77%) are backed by a recorded new tumour event (Recurrence 13, Progression of Disease 3, type missing 4); threshold ≥ 75%. The other 6 are deaths counted as progression; none is unclear.
- **P2 — FAILED (narrowly).** The strict combined label covers 367 of 489 patients (104 resistant / 263 sensitive); predicted ≥ 370.
- **P3 — held.** Broad → strict combined reference: OS18 sensitivity 0.27 → 0.24, PPV 0.78 → 0.80; OS24 sensitivity 0.44 → 0.41, PPV 0.73 → 0.75. All within 0.05.
- **P4 — FAILED.** 1 of the 4 disagreements has a flag or a near-threshold interval: TCGA-24-2029 (154 d). The other three, TCGA-29-1774 (101 d), TCGA-61-2009 (18 d) and TCGA-61-2113 (148 d), are clean resistant calls (recorded Recurrence, no flag) that TCGA's platinum status records as Sensitive. They are not reconstruction artefacts that this audit can detect, and the available data do not explain them.

Decision (pre-specified rule): P1 held, but 27/117 (23%) of the added patients are not clean (> 20%; 33% under the header's definition). The manuscript therefore recommends the STRICT combined label (355, per the resolution above) as primary and reports the broad combined label (394) as a sensitivity analysis. It reports the provenance classes of the added patients and of the 4 disagreements, and the per-patient provenance table is released with the label resource.

# A15b: correction run of A15 (near-threshold flag)

*Status:* post hoc correction of an implementation error in A15; no new predictions. *Script:* `label_validity/15b_reconstruction_provenance_specfix.py`. *Summary:* `label_validity/outputs/15b_reconstruction_provenance_specfix_summary.md`.

## Header (verbatim)

```text
label_validity/15b_reconstruction_provenance_specfix.py
───────────────────────────────────────────────────────
A15b — correction run of A15 (15_reconstruction_provenance.py, committed d349b2b) so that the code matches
A15's pre-registered definition.

Written 2026-10-29 ~22:35 ET, AFTER the A15 run (22:00 ET) and after its results were seen. While filling the
A15 scorecard we found that A15's header lists "interval within 150–215 days (near the 183-day cut-off)" among
the flags and defines "clean" as "no flag", but the code left near_threshold out of any_flag. Aaron decided
(2026-10-29) that the manuscript follows the header's definition. This script is A15 with exactly one change to
the analysis: near_threshold enters any_flag. Outputs carry the prefix a15b_ so A15's outputs are kept unchanged.
No new predictions are made; A15's P1–P4 and decision rule are scored in 15_reconstruction_provenance_summary.md.

Run (from the repo root; no model fitting): python label_validity/15b_reconstruction_provenance_specfix.py --data-root "<...>/OV Data/Project data"
Outputs → label_validity/outputs/a15b_provenance.csv, a15b_class_by_group.csv, a15b_resistant_event_source.csv,
          a15b_os_test_strict.csv, a15b_label_combined_strict.csv, 15b_reconstruction_provenance_specfix_summary.md
```

## Summary: results and scorecard (verbatim)

# A15b — Provenance of the re-derived platinum-free-interval label (correction run: near-threshold intervals flagged, per A15's header)

Re-derived interval determinate: 389; overlap with platinum status: 272; added by reconstruction: 117 (26 resistant).

## Provenance class by group and label

```
provenance_class                             clean_resistant  clean_sensitive  flagged  negative_interval  All
group                        label_pfiplat6                                                                   
added_by_reconstruction      0.0                           0               66       25                  0   91
                             1.0                          12                0       13                  1   26
overlap_with_platinum_status 0.0                           0              143       40                  0  183
                             1.0                          61                0       21                  7   89
All                                                       73              209       99                  8  389
```

## Event source of resistant calls

```
event_source                  death_counted_as_progression  recorded_new_tumour_event:Progression of Disease  recorded_new_tumour_event:Recurrence  recorded_new_tumour_event:nan  All
group                                                                                                                                                                                 
added_by_reconstruction                                  6                                                 3                                    13                              4   26
overlap_with_platinum_status                             0                                                12                                    77                              0   89
All                                                      6                                                15                                    90                              4  115
```

Added resistant calls backed by a recorded new tumour event: 20/26.
Added patients classed clean: 78/117.
Strict combined label: 355 determinate (99 resistant / 256 sensitive).

## The disagreements between platinum status and the re-derived interval

```
                                     group  label_platinum  label_pfiplat6  pfi_from_platinum_d                          event_source provenance_class  redacted  adj_platinum_rows  adj_platinum_stop_missing  later_line_before_event  near_threshold  disagreement src_platinum_status_raw
PATIENT_ID                                                                                                                                                                                                                                                                                   
TCGA-24-2029  overlap_with_platinum_status             0.0             1.0                154.0  recorded_new_tumour_event:Recurrence          flagged     False                  1                      False                    False            True          True               Sensitive
TCGA-29-1774  overlap_with_platinum_status             0.0             1.0                101.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  3                      False                    False           False          True               Sensitive
TCGA-61-2009  overlap_with_platinum_status             0.0             1.0                 18.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
TCGA-61-2113  overlap_with_platinum_status             0.0             1.0                148.0  recorded_new_tumour_event:Recurrence  clean_resistant     False                  1                      False                    False           False          True               Sensitive
```

## OS thresholds as tests: broad vs strict combined reference

- label_os18_all vs label_hybrid (n 375): sensitivity 29/108 = 0.27 [0.19, 0.36]; PPV 29/37 = 0.78 [0.63, 0.89]
- label_os24_all vs label_hybrid (n 360): sensitivity 47/107 = 0.44 [0.35, 0.53]; PPV 47/64 = 0.73 [0.62, 0.83]
- label_os18_all vs label_combined_strict (n 340): sensitivity 22/94 = 0.23 [0.16, 0.33]; PPV 22/28 = 0.79 [0.60, 0.90]
- label_os24_all vs label_combined_strict (n 327): sensitivity 38/93 = 0.41 [0.31, 0.51]; PPV 38/51 = 0.75 [0.61, 0.84]

## Note

Correction run; no new predictions. A15's predictions and decision rule are scored in 15_reconstruction_provenance_summary.md.

# A16: controlled comparison of training labels

*Status:* pre-specified after external review; deposited before running (d349b2b). *Script:* `label_validity/16_controlled_label_comparison.py`. *Summary:* `label_validity/outputs/16_controlled_label_comparison_summary.md`.

## Header (verbatim)

```text
label_validity/16_controlled_label_comparison.py
────────────────────────────────────────────────
A16 — controlled comparison of training labels for expression classifiers: same patients, same outer
folds, paired AUC differences with patient-bootstrap confidence intervals.

Written 2026-10-29 ~22:10 ET, BEFORE the run, in response to an external review of manuscript v5
(point 4: "the classifier experiment does not cleanly isolate the effect of label choice … report paired
uncertainty for the AUC differences"). A5 compared labels on different patient sets and class balances;
its pre-specified rule found a label effect of +0.060 that reached 0.05 in only 3 of 5 repeats.

DISCLOSURE — seen before writing: all A5 results (a5_cross_label_repeats.csv). Not seen: any analysis
restricted to a common patient set, any paired difference, any bootstrap interval for a difference.

Population: platinum-treated patients with RNA-seq data (labels_master in_rnaseq) in whom label_platinum,
label_os18 and label_os24 are ALL determinate. Every label is therefore trained and evaluated on exactly
the same patients.
Pipeline: identical to A5 (05_cross_label_cv.py): log2(RSEM + 1); the genes shared with GSE63885;
500 highest-variance genes and StandardScaler fitted on the training fold only; LR, RF, SVM from
config/config.yaml (balanced class weights, seed 42).
Folds: 20 repeats of stratified 5-fold CV (stratified on label_platinum; random_state = repeat). In each
training fold, one model per training label is fitted on the same training patients; all are scored on the
same held-out patients.
Quantities (all on the same patients):
  * Per repeat: pooled out-of-fold AUC for each training label × model × target label.
  * Primary: ΔAUC_24 = AUC(platinum-trained → platinum status) − AUC(OS24-trained → platinum status),
    mean over the three models. Secondary: ΔAUC_18 (OS18-trained), and the reverse on the OS24 target:
    AUC(OS24-trained → OS24) − AUC(platinum-trained → OS24).
  * Uncertainty: for each model, out-of-fold scores are averaged over the 20 repeats (one score per patient);
    the mean-over-models ΔAUC is recomputed in 2,000 bootstrap resamples of patients stratified by the target
    label (numpy default_rng(42)); 95% percentile interval. The spread of ΔAUC across repeats is reported
    separately and is NOT a confidence interval.

PREDICTIONS
  Q1  Mean ΔAUC_24 (platinum-trained minus OS24-trained, on platinum status) lies between 0 and +0.10.
  Q2  The 95% bootstrap interval for ΔAUC_24 includes 0.
  Q3  ΔAUC_18 > 0, with a 95% interval that includes 0.
  Q4  Reverse on the OS24 target: AUC(OS24-trained) − AUC(platinum-trained) > 0, with a 95% interval
      that includes 0.

DECISION RULES (for the manuscript)
  * If the ΔAUC_24 interval excludes 0 (positive), the manuscript states that, in the same patients,
    platinum-trained models predicted platinum status better than OS-trained models, with the estimate and
    interval.
  * If it includes 0, the manuscript states that a difference larger than the interval's upper bound is
    unlikely but that no difference was detected, and it withdraws any claim that label choice changes
    classifier performance; A5 is then reported as descriptive only.

Run (Windows host, pinned environment; from the repo root):
  & "C:\\Users\\AMAC_WORK\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" label_validity\\16_controlled_label_comparison.py --data-dir "C:\\PROJECTS\\OV Data\\Project data\\ov_tcga_pan_can_atlas_2018"
Outputs → label_validity/outputs/a16_repeats.csv, a16_oof_scores.csv, a16_paired_differences.csv,
          a16_ENVIRONMENT.txt, 16_controlled_label_comparison_summary.md
```

## Summary: results and scorecard (verbatim)

# A16 — Controlled comparison of training labels (same patients, same folds)

Python 3.14.5; scikit-learn 1.9.0; numpy 2.4.6; pandas 3.0.3
Patients: 134 (platinum-resistant 39; OS18 7; OS24 18). 20 × 5-fold CV; 2000 stratified patient bootstraps.

## Mean AUC over 3 models and 20 repeats (min–max across model × repeat)

```
                                mean    min    max
train_label    test_label                         
label_os18     label_os18      0.573  0.155  0.813
               label_os24      0.588  0.318  0.741
               label_platinum  0.540  0.473  0.619
label_os24     label_os18      0.641  0.468  0.755
               label_os24      0.620  0.409  0.724
               label_platinum  0.619  0.541  0.666
label_platinum label_os18      0.593  0.399  0.721
               label_os24      0.655  0.453  0.770
               label_platinum  0.602  0.392  0.703
```

## Paired differences (mean over models; scores averaged over repeats)

- primary_dAUC24 (label_platinum − label_os24 on label_platinum): -0.005 [-0.105, +0.087]; CI includes 0: True; per-repeat mean -0.016 (range -0.107 to +0.071; ≥ 0.05 in 2/20)
- dAUC18 (label_platinum − label_os18 on label_platinum): +0.080 [-0.045, +0.201]; CI includes 0: True; per-repeat mean +0.063 (range -0.014 to +0.145; ≥ 0.05 in 13/20)
- reverse_OS24_target (label_os24 − label_platinum on label_os24): -0.069 [-0.236, +0.081]; CI includes 0: True; per-repeat mean -0.034 (range -0.169 to +0.045; ≥ 0.05 in 0/20)

## Prediction scorecard

~~(to be completed after the run)~~

Run 2026-10-29 21:57–21:59 ET on the Windows host (Python 3.14.5; scikit-learn 1.9.0; numpy 2.4.6; pandas 3.0.3; a16_ENVIRONMENT.txt), after the script with its predictions and decision rules was committed (d349b2b, 21:56:39 ET; now on GitHub main). Output modification times run from 21:57:04 (a16_ENVIRONMENT.txt) to 21:59:39 (a16_paired_differences.csv, this summary, a16_run_log.txt).

Correction to the script header: it says "Written 2026-10-29 ~22:10 ET, BEFORE the run". That time was a wrong estimate. The script was committed at 21:56:39 ET (d349b2b), so it was written before then. The commit timestamp is authoritative, and the run followed it.

Deviation: the script stopped with a UnicodeEncodeError at its final `print` (line 180), because the Windows cp1252 console cannot encode U+2212 (minus sign; traceback in a16_run_log.txt). This summary is written on line 179, before the print, and contains every pre-specified section; all outputs have modification times at or before the crash (21:59:39). No number is affected. Future runs set `PYTHONIOENCODING=utf-8`.

Environment check (run after the scorecard was first drafted, 2026-10-29 ~22:25 ET): the same script was rerun unchanged in the cloud-linked VM (Python 3.10.12; scikit-learn 1.7.2; numpy 2.2.6; pandas 2.3.3); outputs in `a16_env_check_vm/`. Logistic regression and SVM AUCs are identical in all 180 model × label × repeat cells each; Random Forest AUCs differ by up to 0.136 in single cells. Paired differences, Windows → VM: ΔAUC_24 −0.005 → −0.008 [−0.106, +0.086]; ΔAUC_18 +0.080 → +0.074 [−0.050, +0.194]; reverse on OS24 −0.069 → −0.072 [−0.236, +0.077]. Every interval still includes 0 and every prediction scores the same; the Windows run remains the reported result.

Population: 134 patients in whom platinum status, OS18 and OS24 are all determinate (platinum-resistant 39; OS18 7; OS24 18). With only 7 OS18 positives, the OS18-trained models are unstable (OS18-trained → OS18 AUC 0.155–0.813 across model × repeat).

- **Q1 — FAILED.** ΔAUC_24 (platinum-trained − OS24-trained, on platinum status): −0.005 [−0.105, +0.087]; predicted between 0 and +0.10. Per-repeat mean −0.016 (range −0.107 to +0.071; ≥ 0.05 in 2/20).
- **Q2 — held.** The 95% bootstrap interval for ΔAUC_24 includes 0.
- **Q3 — held.** ΔAUC_18 (platinum-trained − OS18-trained, on platinum status): +0.080 [−0.045, +0.201]; > 0, interval includes 0. Per-repeat mean +0.063 (range −0.014 to +0.145; ≥ 0.05 in 13/20).
- **Q4 — FAILED (opposite direction).** On the OS24 target, OS24-trained − platinum-trained: −0.069 [−0.236, +0.081]; predicted > 0. The interval includes 0. Per-repeat mean −0.034 (range −0.169 to +0.045; ≥ 0.05 in 0/20).

Decision (pre-specified rule): the ΔAUC_24 interval includes 0. The manuscript states that, in the same 134 patients with the same folds, no difference was detected between platinum-trained and OS24-trained models in predicting platinum status, and that a platinum-label advantage larger than +0.087 AUC (the interval's upper bound) is unlikely. It withdraws any claim that label choice changes classifier performance; A5 is reported as descriptive only.

# A17: patient-level label table (S11 Table)

*Status:* descriptive assembly; no predictions. *Script:* `label_validity/17_label_resource.py`.

## Header (verbatim)

```text
label_validity/17_label_resource.py
───────────────────────────────────
Builds the versioned, patient-level label resource released with the paper (S11 Table; Zenodo record).
Written 2026-10-29 ~22:45 ET, after A15/A15b/A16, in response to point 6 of the external review of manuscript
v5 (make the label table the main deliverable). Descriptive assembly only: no new analysis, no predictions.
Every column is copied from an existing output; nothing is recomputed except the counts table (event types missing in TCGA-CDR are written as type_not_recorded).

Inputs (label_validity/outputs/): labels_full.csv, labels_master.csv (pfi_from_platinum_d),
  a15b_provenance.csv (provenance class, event source and flags, header definition of "clean"),
  a15b_label_combined_strict.csv (strict combined label, primary; 355 determinate),
  a15_label_combined_strict.csv (strict label as first run, before the near-threshold correction; 367).
Outputs → label_validity/outputs/label_resource_v1.csv, label_resource_v1_dictionary.csv,
          label_resource_v1_counts.csv
Run (from the repo root): python label_validity/17_label_resource.py
```

# A7: feature-selection leakage rerun in the pinned environment

*Status:* pre-specified (pre-run note written before the run).

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

