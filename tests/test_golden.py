"""
Unit Tests for Golden Dataset Constraints & Schema Integrity
-------------------------------------------------------------
Verifies row count, grain uniqueness, account representation, and non-negativity.
Baseline Scope: Exactly 210,000 rows (30,000 accounts x 7 complete baseline months).
"""

import os
import pandas as pd
import pytest

@pytest.fixture
def golden_dataset():
    output_path = os.path.join("outputs", "golden_account_month.csv")
    if not os.path.exists(output_path):
        pytest.fail(f"Golden dataset output file not found at {output_path}. Run build_golden.py first.")
    return pd.read_csv(output_path)

def test_golden_grain_uniqueness(golden_dataset):
    """Assert unique composite primary key (account_id, month)."""
    duplicates = golden_dataset.duplicated(subset=["account_id", "month"]).sum()
    assert duplicates == 0, f"Found {duplicates} duplicate account-month rows in Golden Dataset!"

def test_golden_row_count(golden_dataset):
    """Assert baseline size = number_of_accounts x number_of_complete_months = 30,000 x 7 = 210,000."""
    num_accounts = golden_dataset["account_id"].nunique()
    num_months = golden_dataset["month"].nunique()
    expected_rows = num_accounts * num_months
    
    assert num_accounts == 30000, f"Expected 30,000 accounts, got {num_accounts}"
    assert num_months == 7, f"Expected 7 complete baseline months, got {num_months}"
    assert len(golden_dataset) == expected_rows, f"Expected {expected_rows} rows, got {len(golden_dataset):,}"

def test_all_accounts_represented(golden_dataset):
    """Assert all 30,000 active accounts are represented across baseline months."""
    accounts = pd.read_csv(os.path.join("data", "raw", "accounts.csv"))
    expected_account_ids = set(accounts["account_id"].unique())
    actual_account_ids = set(golden_dataset["account_id"].unique())
    
    assert actual_account_ids == expected_account_ids, "Missing accounts in Golden Dataset account-month grid!"

def test_seven_complete_months(golden_dataset):
    """Assert exact 7 complete baseline months (Jan 2026 - Jul 2026)."""
    expected_months = {"2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07"}
    actual_months = set(golden_dataset["month"].unique())
    assert actual_months == expected_months, f"Expected baseline months {expected_months}, got {actual_months}"

def test_non_negative_recovery(golden_dataset):
    """Assert no negative recovery amounts exist."""
    assert (golden_dataset["clean_recovery_amount"] >= 0).all(), "Found negative clean recovery amounts in Golden Dataset!"
    assert (golden_dataset["raw_recovery_amount"] >= 0).all(), "Found negative raw recovery amounts in Golden Dataset!"
