"""
test_label_investigation.py
─────────────────────────────
Unit tests for label_investigation.py — synthetic data only, no TCGA
files required.

Run with: pytest tests/ -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.label_investigation import (
    check_within_patient_consistency,
    cross_tabulate_against_os_labels,
    map_therapy_outcome_to_binary,
    report_column_coverage,
    report_recall_on_confirmed_nonresponders,
    report_value_distribution,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def timeline_df():
    return pd.DataFrame(
        {
            "PATIENT_ID": ["P1", "P1", "P2", "P3", "P4", "P5"],
            "PRIMARY_THERAPY_OUTCOME_SUCCESS": [
                "Complete Remission/Response",
                "Complete Remission/Response",  # consistent repeat for P1
                "Progressive Disease",
                "Partial Remission/Response",
                "Stable Disease",
                np.nan,
            ],
            "CLINICAL_STAGE": ["IIIC", "IIIC", "IV", "IIIC", "IIIC", np.nan],
            "TUMOR_STATUS": ["TUMOR FREE", "TUMOR FREE", "WITH TUMOR", "WITH TUMOR", "TUMOR FREE", np.nan],
        }
    )


@pytest.fixture
def conflicting_timeline_df():
    return pd.DataFrame(
        {
            "PATIENT_ID": ["P1", "P1"],
            "PRIMARY_THERAPY_OUTCOME_SUCCESS": [
                "Complete Remission/Response",
                "Progressive Disease",  # conflicting second entry
            ],
        }
    )


# ─────────────────────────────────────────────────────────────────────────────
# report_column_coverage
# ─────────────────────────────────────────────────────────────────────────────


class TestReportColumnCoverage:
    def test_overall_coverage_counts(self, timeline_df):
        result = report_column_coverage(timeline_df, ["PRIMARY_THERAPY_OUTCOME_SUCCESS"])
        row = result.iloc[0]
        assert row["n_total_rows"] == 6
        assert row["n_non_null"] == 5  # one NaN (P5)

    def test_platinum_cohort_restriction(self, timeline_df):
        platinum_ids = np.array(["P1", "P2"])
        result = report_column_coverage(
            timeline_df, ["PRIMARY_THERAPY_OUTCOME_SUCCESS"], platinum_ids=platinum_ids
        )
        row = result.iloc[0]
        # P1 appears twice, P2 once → 3 rows in platinum cohort, all non-null
        assert row["n_platinum_cohort_rows"] == 3
        assert row["n_non_null_platinum_cohort"] == 3

    def test_missing_column_is_skipped_not_crashed(self, timeline_df):
        result = report_column_coverage(timeline_df, ["NONEXISTENT_COLUMN"])
        assert len(result) == 0


# ─────────────────────────────────────────────────────────────────────────────
# report_value_distribution
# ─────────────────────────────────────────────────────────────────────────────


class TestReportValueDistribution:
    def test_counts_match_expected(self, timeline_df):
        counts = report_value_distribution(timeline_df, "PRIMARY_THERAPY_OUTCOME_SUCCESS")
        assert counts["Complete Remission/Response"] == 2

    def test_missing_column_raises(self, timeline_df):
        with pytest.raises(KeyError):
            report_value_distribution(timeline_df, "NONEXISTENT_COLUMN")


# ─────────────────────────────────────────────────────────────────────────────
# check_within_patient_consistency
# ─────────────────────────────────────────────────────────────────────────────


class TestCheckWithinPatientConsistency:
    def test_consistent_patient_not_flagged(self, timeline_df):
        result = check_within_patient_consistency(timeline_df, "PRIMARY_THERAPY_OUTCOME_SUCCESS")
        # P1 has 2 rows but they agree → not a conflict
        assert result["n_patients_with_conflicting_values"] == 0
        assert result["n_patients_with_multiple_non_null_rows"] == 1

    def test_conflicting_patient_flagged(self, conflicting_timeline_df):
        result = check_within_patient_consistency(conflicting_timeline_df, "PRIMARY_THERAPY_OUTCOME_SUCCESS")
        assert result["n_patients_with_conflicting_values"] == 1
        assert "P1" in result["example_conflicting_patient_ids"]


# ─────────────────────────────────────────────────────────────────────────────
# map_therapy_outcome_to_binary
# ─────────────────────────────────────────────────────────────────────────────


class TestMapTherapyOutcomeToBinary:
    def test_complete_response_maps_to_zero(self, timeline_df):
        mapped = map_therapy_outcome_to_binary(timeline_df)
        assert mapped.loc["P1"] == 0

    def test_progressive_disease_maps_to_one(self, timeline_df):
        mapped = map_therapy_outcome_to_binary(timeline_df)
        assert mapped.loc["P2"] == 1

    def test_ambiguous_categories_map_to_nan(self, timeline_df):
        mapped = map_therapy_outcome_to_binary(timeline_df)
        assert pd.isna(mapped.loc["P3"])  # Partial Remission/Response
        assert pd.isna(mapped.loc["P4"])  # Stable Disease

    def test_nan_input_not_included(self, timeline_df):
        mapped = map_therapy_outcome_to_binary(timeline_df)
        assert "P5" not in mapped.index  # was NaN in the source, dropped before grouping


# ─────────────────────────────────────────────────────────────────────────────
# cross_tabulate_against_os_labels
# ─────────────────────────────────────────────────────────────────────────────


class TestCrossTabulateAgainstOsLabels:
    @pytest.fixture
    def candidate_labels(self):
        return pd.Series({"P1": 0, "P2": 1, "P6": 0}, name="PRIMARY_THERAPY_OUTCOME_SUCCESS")

    @pytest.fixture
    def os_labelled_dict(self):
        return {
            12: pd.DataFrame({"PATIENT_ID": ["P1", "P2", "P7"], "response": [0, 1, 0]}),
            24: pd.DataFrame({"PATIENT_ID": ["P1", "P2"], "response": [1, 1]}),  # P1 disagrees here
        }

    def test_full_agreement_threshold(self, candidate_labels, os_labelled_dict):
        result = cross_tabulate_against_os_labels(candidate_labels, os_labelled_dict)
        row_12 = result[result["threshold_m"] == 12].iloc[0]
        assert row_12["n_overlap"] == 2  # P1, P2 (P6 and P7 don't overlap)
        assert row_12["pct_agree"] == 100.0

    def test_partial_agreement_threshold(self, candidate_labels, os_labelled_dict):
        result = cross_tabulate_against_os_labels(candidate_labels, os_labelled_dict)
        row_24 = result[result["threshold_m"] == 24].iloc[0]
        assert row_24["n_overlap"] == 2
        assert row_24["n_agree"] == 1  # only P2 agrees; P1 disagrees (0 vs 1)

    def test_no_overlap_is_skipped(self, candidate_labels):
        os_labelled_dict = {12: pd.DataFrame({"PATIENT_ID": ["P99"], "response": [0]})}
        result = cross_tabulate_against_os_labels(candidate_labels, os_labelled_dict)
        assert len(result) == 0


# ─────────────────────────────────────────────────────────────────────────────
# report_recall_on_confirmed_nonresponders
# ─────────────────────────────────────────────────────────────────────────────


class TestReportRecallOnConfirmedNonresponders:
    @pytest.fixture
    def candidate_labels_with_confirmed_cases(self):
        # 3 confirmed non-responders (label=1), rest responders (label=0)
        return pd.Series(
            {"P1": 1, "P2": 1, "P3": 1, "P4": 0, "P5": 0},
            name="PRIMARY_THERAPY_OUTCOME_SUCCESS",
        )

    def test_perfect_recall(self, candidate_labels_with_confirmed_cases):
        # OS proxy correctly flags all 3 confirmed non-responders as 1
        os_labelled_dict = {
            12: pd.DataFrame({"PATIENT_ID": ["P1", "P2", "P3", "P4"], "response": [1, 1, 1, 0]})
        }
        result = report_recall_on_confirmed_nonresponders(candidate_labels_with_confirmed_cases, os_labelled_dict)
        row = result.iloc[0]
        assert row["n_confirmed_nonresponders"] == 3
        assert row["recall"] == 1.0

    def test_partial_recall_identifies_missed_patients(self, candidate_labels_with_confirmed_cases):
        # OS proxy misses P2 (flags as responder=0 when truly non-responder)
        os_labelled_dict = {
            12: pd.DataFrame({"PATIENT_ID": ["P1", "P2", "P3"], "response": [1, 0, 1]})
        }
        result = report_recall_on_confirmed_nonresponders(candidate_labels_with_confirmed_cases, os_labelled_dict)
        row = result.iloc[0]
        assert row["recall"] == pytest.approx(2 / 3, abs=0.001)
        assert "P2" in row["missed_patient_ids"]

    def test_no_overlap_skipped(self, candidate_labels_with_confirmed_cases):
        os_labelled_dict = {12: pd.DataFrame({"PATIENT_ID": ["P99"], "response": [0]})}
        result = report_recall_on_confirmed_nonresponders(candidate_labels_with_confirmed_cases, os_labelled_dict)
        assert len(result) == 0
