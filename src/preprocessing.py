"""
preprocessing.py
────────────────
All data-cleaning and label-engineering logic.

Steps performed here:
  1. Extract and clean survival columns from clinical data.
  2. Identify platinum-treated patients from the treatment timeline.
  3. Assign binary response labels at one or more time thresholds.
  4. Clean and align the mRNA expression matrix.
"""

from __future__ import annotations

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Survival data
# ─────────────────────────────────────────────────────────────────────────────


def extract_survival(
    clinical: pd.DataFrame,
    time_col: str,
    status_col: str,
) -> pd.DataFrame:
    """
    Pull survival columns from clinical data and create a binary event flag.

    ``event = 1`` → patient died (DECEASED / DEAD / 1:DECEASED …)
    ``event = 0`` → patient alive / censored

    Args:
        clinical:   Raw clinical DataFrame.
        time_col:   Name of the survival-time column (e.g. ``OS_MONTHS``).
        status_col: Name of the status column (e.g. ``OS_STATUS``).

    Returns:
        DataFrame with columns [PATIENT_ID, <time_col>, event].
    """
    _validate_columns(clinical, ["PATIENT_ID", time_col, status_col])

    surv = clinical[["PATIENT_ID", time_col, status_col]].copy()
    surv[time_col] = pd.to_numeric(surv[time_col], errors="coerce")

    # Handles: "DECEASED", "DEAD", "1:DECEASED", "1:DEAD", raw "1"
    status_upper = surv[status_col].astype(str).str.upper()
    surv["event"] = (
        status_upper.str.contains("DECEASED")
        | status_upper.str.contains("DEAD")
        | status_upper.str.fullmatch(r"1.*", na=False)
    ).astype(int)

    logger.info(
        "Survival extracted: %d patients | %d events",
        len(surv),
        surv["event"].sum(),
    )
    return surv.drop(columns=[status_col])


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Platinum treatment
# ─────────────────────────────────────────────────────────────────────────────


def identify_platinum_patients(
    treatment: pd.DataFrame,
    platinum_drugs: list[str],
) -> np.ndarray:
    """
    Return unique patient IDs who received any platinum-based drug.

    Args:
        treatment:      Raw treatment-timeline DataFrame.
        platinum_drugs: List of drug names (case-insensitive).

    Returns:
        Sorted array of unique PATIENT_ID strings.
    """
    _validate_columns(treatment, ["PATIENT_ID", "AGENT"])

    drugs_upper = [d.upper() for d in platinum_drugs]
    mask = treatment["AGENT"].astype(str).str.upper().isin(drugs_upper)

    platinum_ids = treatment.loc[mask, "PATIENT_ID"].dropna().unique()
    logger.info("Platinum-treated patients identified: %d", len(platinum_ids))
    return np.sort(platinum_ids)


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Response labelling
# ─────────────────────────────────────────────────────────────────────────────


def assign_response_label(
    surv: pd.DataFrame,
    time_col: str,
    threshold: float,
) -> pd.Series:
    """
    Vectorised label assignment for a single time threshold.

    Label rules
    ───────────
    ``1`` (non-responder / early death): event == 1 AND time < threshold
    ``0`` (responder / survived):        time >= threshold   (any event status)
    ``NaN`` (ambiguous):                 time < threshold AND event == 0 (censored early)

    Args:
        surv:      DataFrame that includes the time column and ``event``.
        time_col:  Name of the OS/DFS/… months column.
        threshold: Cutoff in months.

    Returns:
        A Series of {0, 1, NaN} aligned to ``surv.index``.
    """
    t = surv[time_col]
    e = surv["event"]

    label = pd.Series(np.nan, index=surv.index)
    label[t >= threshold] = 0                    # survived past cutoff
    label[(t < threshold) & (e == 1)] = 1        # died before cutoff

    n_labelled = label.notna().sum()
    n_nan = label.isna().sum()
    logger.info(
        "Threshold=%dm → 0 (responder): %d | 1 (non-responder): %d | NaN: %d",
        int(threshold),
        (label == 0).sum(),
        (label == 1).sum(),
        n_nan,
    )
    return label


def build_labelled_survival(
    surv: pd.DataFrame,
    platinum_ids: np.ndarray,
    time_col: str,
    thresholds: list[float],
) -> dict[int, pd.DataFrame]:
    """
    Build a labelled survival table for each threshold.

    Filters to platinum-treated patients first, then creates
    a separate DataFrame per threshold containing only fully
    labelled rows.

    Args:
        surv:          Output of :func:`extract_survival`.
        platinum_ids:  Output of :func:`identify_platinum_patients`.
        time_col:      Survival-time column name.
        thresholds:    List of month cutoffs (e.g. [12, 18, 24]).

    Returns:
        Dict mapping threshold → labelled DataFrame
        (columns: PATIENT_ID, <time_col>, event, response).
    """
    surv_plat = surv[surv["PATIENT_ID"].isin(platinum_ids)].copy()
    logger.info("Platinum patients with survival data: %d", len(surv_plat))

    labelled: dict[int, pd.DataFrame] = {}
    for thr in thresholds:
        col = f"response_{int(thr)}m"
        df = surv_plat.copy()
        df[col] = assign_response_label(df, time_col, thr)
        df = df.dropna(subset=[col]).copy()
        df[col] = df[col].astype(int)
        df = df.rename(columns={col: "response"})
        labelled[int(thr)] = df
        logger.info("Threshold %dm → %d labelled patients", int(thr), len(df))

    return labelled


# ─────────────────────────────────────────────────────────────────────────────
# 4.  Expression matrix
# ─────────────────────────────────────────────────────────────────────────────


def clean_expression(expr_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw RSEM expression table into a genes × patients DataFrame.

    Steps:
      - Set ``Hugo_Symbol`` as the gene index.
      - Drop ``Entrez_Gene_Id``.
      - Truncate sample barcodes to 12 characters (TCGA patient ID).
      - Average duplicate samples for the same patient.

    Args:
        expr_raw: Raw expression DataFrame (genes × samples).

    Returns:
        Clean expression DataFrame (genes × patients).
    """
    expr = (
        expr_raw
        .set_index("Hugo_Symbol")
        .drop(columns=["Entrez_Gene_Id"], errors="ignore")
    )

    # Truncate TCGA sample IDs → 12-char patient IDs
    expr.columns = expr.columns.str.slice(0, 12)

    # Average any duplicate samples for the same patient (pandas ≥ 2.0 safe)
    expr = expr.T.groupby(level=0).mean().T

    # Real Hugo_Symbol gene lists occasionally contain entries that pandas/
    # downstream tools coerce inconsistently (e.g. mixed str/object dtypes
    # after the groupby/transpose above). Coercing to str here, once, at
    # the source, avoids fragile column-type mismatches in every consumer
    # downstream (this surfaced as a real bug in src/ablation.py's
    # supervised F-score selection when run on the actual TCGA file).
    expr.index = expr.index.astype(str)

    logger.info(
        "Expression cleaned: %d genes × %d patients",
        expr.shape[0],
        expr.shape[1],
    )
    return expr


def align_expression_to_labels(
    expr: pd.DataFrame,
    labelled: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Subset and align the expression matrix to a labelled survival DataFrame.

    Args:
        expr:     Clean expression DataFrame (genes × patients).
        labelled: Output of :func:`build_labelled_survival` for one threshold.

    Returns:
        (X, y) where X is (patients × genes) and y is a Series of 0/1 labels,
        both indexed by PATIENT_ID, sorted consistently.
    """
    labelled_ids = labelled["PATIENT_ID"].unique()
    common = sorted(set(expr.columns).intersection(labelled_ids))

    if not common:
        raise ValueError(
            "No patients overlap between expression matrix and labelled survival data."
        )

    X = expr[common].T                                          # patients × genes
    y = labelled.set_index("PATIENT_ID").loc[common, "response"]

    logger.info(
        "Aligned dataset: %d patients × %d genes | class counts: %s",
        X.shape[0],
        X.shape[1],
        y.value_counts().to_dict(),
    )
    return X, y


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _validate_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Required columns missing from DataFrame: {missing}")
