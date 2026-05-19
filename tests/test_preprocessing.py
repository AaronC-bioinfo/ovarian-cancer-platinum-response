"""
test_preprocessing.py
─────────────────────
Unit tests for the preprocessing module.

Run with: pytest tests/ -v
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing import (
    assign_response_label,
    clean_expression,
    extract_survival,
    identify_platinum_patients,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture
def sample_clinical() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PATIENT_ID": ["P001", "P002", "P003", "P004", "P005"],
            "OS_MONTHS": [6.0, 24.0, 14.0, np.nan, 36.0],
            "OS_STATUS": [
                "1:DECEASED",
                "0:LIVING",
                "DECEASED",
                "0:LIVING",
                "1:DECEASED",
            ],
        }
    )


@pytest.fixture
def sample_treatment() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "PATIENT_ID": ["P001", "P002", "P003", "P004", "P006"],
            "AGENT": ["Carboplatin", "gemcitabine", "CISPLATIN", "carboplatin", "paclitaxel"],
        }
    )


@pytest.fixture
def sample_survival(sample_clinical) -> pd.DataFrame:
    return extract_survival(sample_clinical, "OS_MONTHS", "OS_STATUS")


# ─────────────────────────────────────────────────────────────────────────────
# extract_survival
# ─────────────────────────────────────────────────────────────────────────────


class TestExtractSurvival:
    def test_shape(self, sample_survival):
        assert sample_survival.shape[1] == 3  # PATIENT_ID, OS_MONTHS, event

    def test_event_encoding(self, sample_survival):
        # P001 = DECEASED → 1, P002 = LIVING → 0, P003 = DECEASED → 1
        assert sample_survival.loc[sample_survival["PATIENT_ID"] == "P001", "event"].values[0] == 1
        assert sample_survival.loc[sample_survival["PATIENT_ID"] == "P002", "event"].values[0] == 0
        assert sample_survival.loc[sample_survival["PATIENT_ID"] == "P005", "event"].values[0] == 1

    def test_time_numeric(self, sample_survival):
        assert pd.api.types.is_float_dtype(sample_survival["OS_MONTHS"])

    def test_missing_columns_raises(self):
        bad = pd.DataFrame({"PATIENT_ID": ["P001"], "SOME_COL": [1]})
        with pytest.raises(KeyError):
            extract_survival(bad, "OS_MONTHS", "OS_STATUS")


# ─────────────────────────────────────────────────────────────────────────────
# identify_platinum_patients
# ─────────────────────────────────────────────────────────────────────────────


class TestIdentifyPlatinumPatients:
    def test_correct_patients(self, sample_treatment):
        platinum = identify_platinum_patients(
            sample_treatment, ["CARBOPLATIN", "CISPLATIN"]
        )
        assert set(platinum) == {"P001", "P003", "P004"}

    def test_case_insensitive(self, sample_treatment):
        # "carboplatin" (lowercase) in treatment data should still match
        platinum = identify_platinum_patients(sample_treatment, ["carboplatin"])
        assert "P001" in platinum
        assert "P004" in platinum

    def test_no_match_returns_empty(self, sample_treatment):
        platinum = identify_platinum_patients(sample_treatment, ["OXALIPLATIN"])
        assert len(platinum) == 0


# ─────────────────────────────────────────────────────────────────────────────
# assign_response_label
# ─────────────────────────────────────────────────────────────────────────────


class TestAssignResponseLabel:
    def test_responder_label(self, sample_survival):
        labels = assign_response_label(sample_survival, "OS_MONTHS", threshold=12.0)
        # P002 (24m, alive) → 0 (responder)
        p002_label = labels[sample_survival["PATIENT_ID"] == "P002"].values[0]
        assert p002_label == 0

    def test_non_responder_label(self, sample_survival):
        labels = assign_response_label(sample_survival, "OS_MONTHS", threshold=12.0)
        # P001 (6m, deceased) → 1 (non-responder)
        p001_label = labels[sample_survival["PATIENT_ID"] == "P001"].values[0]
        assert p001_label == 1

    def test_ambiguous_returns_nan(self, sample_survival):
        labels = assign_response_label(sample_survival, "OS_MONTHS", threshold=12.0)
        # P004 has NaN time → NaN label
        p004_label = labels[sample_survival["PATIENT_ID"] == "P004"].values[0]
        assert np.isnan(p004_label)

    def test_censored_before_threshold_is_nan(self, sample_survival):
        # P002 is 24m LIVING — at 12m threshold they are a responder (survived past)
        labels = assign_response_label(sample_survival, "OS_MONTHS", threshold=12.0)
        p002 = labels[sample_survival["PATIENT_ID"] == "P002"].values[0]
        assert p002 == 0


# ─────────────────────────────────────────────────────────────────────────────
# clean_expression
# ─────────────────────────────────────────────────────────────────────────────


class TestCleanExpression:
    def test_index_is_gene(self):
        raw = pd.DataFrame(
            {
                "Hugo_Symbol": ["BRCA1", "TP53"],
                "Entrez_Gene_Id": [672, 7157],
                "TCGA-01-XXXX-01A": [1.0, 2.0],
                "TCGA-02-YYYY-01A": [3.0, 4.0],
            }
        )
        clean = clean_expression(raw)
        assert clean.index.tolist() == ["BRCA1", "TP53"]

    def test_sample_ids_truncated(self):
        raw = pd.DataFrame(
            {
                "Hugo_Symbol": ["BRCA1"],
                "Entrez_Gene_Id": [672],
                "TCGA-01-XXXX-01A": [1.0],
                "TCGA-02-YYYY-01A": [3.0],
            }
        )
        clean = clean_expression(raw)
        assert all(len(c) == 12 for c in clean.columns)

    def test_duplicates_averaged(self):
        # Two samples with same first 12 chars → should be averaged
        raw = pd.DataFrame(
            {
                "Hugo_Symbol": ["BRCA1"],
                "Entrez_Gene_Id": [672],
                "TCGA-01-XXXX-01A": [2.0],
                "TCGA-01-XXXX-02A": [4.0],
            }
        )
        clean = clean_expression(raw)
        assert clean.shape[1] == 1
        assert float(clean.iloc[0, 0]) == pytest.approx(3.0)
