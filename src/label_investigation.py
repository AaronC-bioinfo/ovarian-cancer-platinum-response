"""
label_investigation.py
───────────────────────
Diagnostic-only analysis of candidate gold-standard label columns found
in data_timeline_status.txt and data_clinical_sample.txt.

This module makes NO changes to the main pipeline or its labels. It exists
to answer one question with evidence: is PRIMARY_THERAPY_OUTCOME_SUCCESS
(or another flagged column) usable as a replacement for the OS-threshold
proxy label currently used in preprocessing.py?

Nothing here is wired into run.py — it's a standalone investigation that
informs whether/how Phase 2 of the publication-upgrade roadmap proceeds.
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def report_column_coverage(
    df: pd.DataFrame,
    columns: list[str],
    patient_id_col: str = "PATIENT_ID",
    platinum_ids: np.ndarray | None = None,
) -> pd.DataFrame:
    """
    Report non-null coverage for a list of candidate columns, both overall
    and restricted to the platinum-treated cohort (if provided).

    Args:
        df:             DataFrame to inspect (e.g. timeline status or
                        clinical sample file).
        columns:        Candidate column names to check.
        patient_id_col: Name of the patient ID column.
        platinum_ids:   Optional array of platinum-treated patient IDs to
                        restrict the "platinum cohort" coverage numbers to.

    Returns:
        DataFrame with columns [column, n_total, n_non_null, pct_non_null,
        n_non_null_platinum_cohort, pct_non_null_platinum_cohort].
    """
    rows = []
    platinum_mask = (
        df[patient_id_col].isin(platinum_ids) if platinum_ids is not None else pd.Series(True, index=df.index)
    )

    for col in columns:
        if col not in df.columns:
            logger.warning("Column '%s' not found in DataFrame — skipping.", col)
            continue

        n_total = len(df)
        n_non_null = df[col].notna().sum()

        platinum_subset = df.loc[platinum_mask, col]
        n_non_null_plat = platinum_subset.notna().sum()
        n_total_plat = len(platinum_subset)

        rows.append(
            {
                "column": col,
                "n_total_rows": n_total,
                "n_non_null": n_non_null,
                "pct_non_null": round(100 * n_non_null / n_total, 1) if n_total else np.nan,
                "n_platinum_cohort_rows": n_total_plat,
                "n_non_null_platinum_cohort": n_non_null_plat,
                "pct_non_null_platinum_cohort": (
                    round(100 * n_non_null_plat / n_total_plat, 1) if n_total_plat else np.nan
                ),
            }
        )

    result = pd.DataFrame(rows)
    logger.info("Column coverage report:\n%s", result.to_string(index=False))
    return result


def report_value_distribution(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Report the value_counts() for a categorical candidate label column,
    including NaN, so the actual category strings are visible (e.g.
    "Complete Remission/Response" vs "Progressive Disease").

    Args:
        df:     DataFrame to inspect.
        column: Column name to report.

    Returns:
        Series of value counts (including NaN).
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found.")

    counts = df[column].value_counts(dropna=False)
    logger.info("Value distribution for '%s':\n%s", column, counts.to_string())
    return counts


def check_within_patient_consistency(
    df: pd.DataFrame,
    column: str,
    patient_id_col: str = "PATIENT_ID",
) -> dict:
    """
    For patients with multiple timeline rows, check whether a candidate
    label column is consistent across rows or varies — this determines
    whether "take the first non-null value per patient" is a safe
    simplification or whether more careful chronological handling
    (e.g. by a sequence/date column) is needed.

    Args:
        df:             DataFrame with potentially multiple rows per patient
                        (e.g. data_timeline_status.txt).
        column:         Candidate label column to check.
        patient_id_col: Name of the patient ID column.

    Returns:
        Dict with keys: n_patients_total, n_patients_with_multiple_rows,
        n_patients_with_conflicting_values, pct_conflicting,
        example_conflicting_patient_ids (up to 5).
    """
    non_null = df[df[column].notna()].copy()
    grouped = non_null.groupby(patient_id_col)[column].nunique()

    n_multi_row_patients = (
        non_null.groupby(patient_id_col).size().gt(1).sum()
    )
    conflicting = grouped[grouped > 1]

    result = {
        "n_patients_total": df[patient_id_col].nunique(),
        "n_patients_with_multiple_non_null_rows": int(n_multi_row_patients),
        "n_patients_with_conflicting_values": int(len(conflicting)),
        "pct_conflicting_among_multi_row": (
            round(100 * len(conflicting) / n_multi_row_patients, 1) if n_multi_row_patients else 0.0
        ),
        "example_conflicting_patient_ids": list(conflicting.index[:5]),
    }
    logger.info("Within-patient consistency check for '%s': %s", column, result)
    return result


def map_therapy_outcome_to_binary(
    df: pd.DataFrame,
    column: str = "PRIMARY_THERAPY_OUTCOME_SUCCESS",
    patient_id_col: str = "PATIENT_ID",
) -> pd.Series:
    """
    Map PRIMARY_THERAPY_OUTCOME_SUCCESS categories to a binary platinum
    response label, ONE ROW PER PATIENT (first non-null value taken).

    Mapping convention (standard in gynecologic oncology literature):
        responder (0):      "Complete Remission/Response"
        non-responder (1):  "Progressive Disease"
        excluded (NaN):     "Partial Remission/Response", "Stable Disease"
                            — these are genuinely ambiguous with respect to
                            platinum sensitivity and are excluded rather than
                            forced into a binary bucket.

    This is a DIAGNOSTIC/CANDIDATE mapping for comparison against the
    existing OS-threshold labels — it is not yet wired into the main
    pipeline.

    Args:
        df:             data_timeline_status.txt (or similar).
        column:         Therapy outcome column name.
        patient_id_col: Patient ID column name.

    Returns:
        Series indexed by PATIENT_ID with values in {0, 1, NaN}.
    """
    mapping = {
        "Complete Remission/Response": 0,
        "Partial Remission/Response": np.nan,
        "Stable Disease": np.nan,
        "Progressive Disease": 1,
    }

    non_null = df[df[column].notna()].copy()
    # First non-null entry per patient (diagnostic simplification — see
    # check_within_patient_consistency to confirm this is safe for your data)
    first_per_patient = non_null.groupby(patient_id_col)[column].first()

    mapped = first_per_patient.map(mapping)
    unmapped_values = first_per_patient[~first_per_patient.isin(mapping.keys())].unique()
    if len(unmapped_values) > 0:
        logger.warning(
            "Found %d category value(s) not in the standard mapping: %s. "
            "These will be NaN — extend the mapping if they're meaningful.",
            len(unmapped_values),
            list(unmapped_values),
        )

    logger.info(
        "Therapy-outcome binary mapping: %d responders (0), %d non-responders (1), %d excluded/NaN",
        (mapped == 0).sum(),
        (mapped == 1).sum(),
        mapped.isna().sum(),
    )
    return mapped


def cross_tabulate_against_os_labels(
    therapy_outcome_labels: pd.Series,
    os_labelled_dict: dict[int, pd.DataFrame],
) -> pd.DataFrame:
    """
    Compare the therapy-outcome-derived label against the existing
    OS-threshold proxy labels at each threshold, for patients where both
    are available.

    A high agreement rate would suggest the OS proxy was a reasonable
    stand-in; a low rate would justify the relabeling effort and should
    be reported as a quantified finding either way.

    Args:
        therapy_outcome_labels: Output of map_therapy_outcome_to_binary,
                                indexed by PATIENT_ID.
        os_labelled_dict:       Output of build_labelled_survival —
                                {threshold: df with PATIENT_ID, response}.

    Returns:
        DataFrame with columns [threshold_m, n_overlap, n_agree, pct_agree,
        cohens_kappa].
    """
    rows = []
    for thr, os_df in os_labelled_dict.items():
        os_labels = os_df.set_index("PATIENT_ID")["response"]

        common_ids = therapy_outcome_labels.dropna().index.intersection(os_labels.index)
        if len(common_ids) == 0:
            logger.warning("No overlapping patients for threshold %dm — skipping.", thr)
            continue

        a = therapy_outcome_labels.loc[common_ids]
        b = os_labels.loc[common_ids]

        agree = (a == b).sum()
        pct_agree = round(100 * agree / len(common_ids), 1)

        # Cohen's kappa — agreement above chance
        kappa = _cohens_kappa(a.values, b.values)

        rows.append(
            {
                "threshold_m": thr,
                "n_overlap": len(common_ids),
                "n_agree": int(agree),
                "pct_agree": pct_agree,
                "cohens_kappa": round(kappa, 3),
            }
        )

    result = pd.DataFrame(rows)
    logger.info("Cross-tabulation vs. OS-threshold labels:\n%s", result.to_string(index=False))
    return result


def _cohens_kappa(a: np.ndarray, b: np.ndarray) -> float:
    """Minimal Cohen's kappa implementation for two binary label arrays."""
    from sklearn.metrics import cohen_kappa_score

    return cohen_kappa_score(a, b)


def report_recall_on_confirmed_nonresponders(
    candidate_labels: pd.Series,
    os_labelled_dict: dict[int, pd.DataFrame],
) -> pd.DataFrame:
    """
    Targeted validation check: among patients with a DOCUMENTED clinical
    non-response (PRIMARY_THERAPY_OUTCOME_SUCCESS == "Progressive Disease",
    i.e. candidate_label == 1), what fraction does the existing
    OS-threshold proxy also flag as a non-responder?

    This is more informative than Cohen's kappa when the confirmed-label
    set is small and extremely imbalanced (e.g. 7 positives out of ~500
    patients) — kappa collapses toward zero under extreme class skew even
    when raw agreement is high, because the chance-agreement term in its
    denominator is dominated by the skew. Recall on the known positives
    answers a sharper, more decision-relevant question: of the patients we
    are MOST confident were truly platinum-resistant, does the OS proxy
    correctly capture them?

    Args:
        candidate_labels: Output of map_therapy_outcome_to_binary, indexed
                          by PATIENT_ID.
        os_labelled_dict: Output of build_labelled_survival —
                          {threshold: df with PATIENT_ID, response}.

    Returns:
        DataFrame with columns [threshold_m, n_confirmed_nonresponders,
        n_overlap_with_os_labels, n_correctly_flagged, recall,
        missed_patient_ids].
    """
    confirmed_nonresponders = candidate_labels[candidate_labels == 1].index

    rows = []
    for thr, os_df in os_labelled_dict.items():
        os_labels = os_df.set_index("PATIENT_ID")["response"]

        overlap = confirmed_nonresponders.intersection(os_labels.index)
        if len(overlap) == 0:
            logger.warning(
                "No confirmed non-responders overlap with OS labels at %dm — skipping.", thr
            )
            continue

        os_subset = os_labels.loc[overlap]
        n_correct = (os_subset == 1).sum()
        recall = n_correct / len(overlap)
        missed = list(overlap[os_subset != 1])

        rows.append(
            {
                "threshold_m": thr,
                "n_confirmed_nonresponders": len(confirmed_nonresponders),
                "n_overlap_with_os_labels": len(overlap),
                "n_correctly_flagged_by_os_proxy": int(n_correct),
                "recall": round(recall, 3),
                "missed_patient_ids": missed,
            }
        )

    result = pd.DataFrame(rows)
    logger.info(
        "Recall of OS-threshold proxy on confirmed non-responders:\n%s",
        result.drop(columns=["missed_patient_ids"], errors="ignore").to_string(index=False),
    )
    return result
