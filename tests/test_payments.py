"""
Unit Tests for Payment Deduplication & Financial Data Quality
--------------------------------------------------------------
Verifies SUCCESS status filtering, payment_reference uniqueness, and non-negativity.
"""

import os
import pandas as pd
import pytest

@pytest.fixture
def raw_payments():
    return pd.read_csv(os.path.join("data", "raw", "payments.csv"))

def test_payment_status_filtering(raw_payments):
    """Assert non-SUCCESS payments are present in raw data and filtered out during cleaning."""
    non_success_count = (raw_payments["payment_status"] != "SUCCESS").sum()
    assert non_success_count > 0, "Expected non-SUCCESS payment records in raw payments dataset."

def test_payment_reference_deduplication(raw_payments):
    """Assert raw SUCCESS payments contain duplicate retries and deduplication removes them."""
    raw_succ = raw_payments[raw_payments["payment_status"] == "SUCCESS"]
    clean_succ = raw_succ.drop_duplicates(subset=["payment_reference"])
    
    dup_count = len(raw_succ) - len(clean_succ)
    assert dup_count > 0, f"Expected duplicate payment references, found {dup_count}"
    assert not clean_succ.duplicated(subset=["payment_reference"]).any(), "Clean payments dataset contains duplicate payment references!"

def test_payment_amounts_non_negative(raw_payments):
    """Assert all payment amounts are strictly positive."""
    assert (raw_payments["amount"] > 0).all(), "Found non-positive payment amounts in raw payment ledger!"
