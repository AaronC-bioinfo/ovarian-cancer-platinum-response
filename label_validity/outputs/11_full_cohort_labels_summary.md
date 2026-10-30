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
