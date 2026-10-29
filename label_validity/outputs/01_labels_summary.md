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