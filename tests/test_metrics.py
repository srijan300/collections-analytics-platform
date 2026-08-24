"""
Unit Tests for KPI Math Reconciliation & Financial Identities
--------------------------------------------------------------
Verifies: raw_recovery - clean_recovery = duplicate_inflation
Verifies: inflation_pct = duplicate_inflation / raw_recovery * 100
Verifies: Feb-Mar MoM clean recovery growth calculation
"""

import os
import pandas as pd
import pytest

@pytest.fixture
def monthly_kpis():
    output_path = os.path.join("outputs", "monthly_kpis.csv")
    if not os.path.exists(output_path):
        pytest.fail(f"Monthly KPIs output file not found at {output_path}. Run build_golden.py first.")
    return pd.read_csv(output_path)

def test_reconciliation_math_identity(monthly_kpis):
    """Assert identity: raw_recovery - clean_recovery = duplicate_inflation."""
    for idx, row in monthly_kpis.iterrows():
        raw = row["raw_recovery_inr"]
        clean = row["clean_recovery_inr"]
        dup = row["duplicate_inflation_inr"]
        
        diff = abs((raw - clean) - dup)
        assert diff < 0.01, f"Reconciliation math mismatch for month {row['month']}: raw={raw}, clean={clean}, dup={dup}"

def test_duplicate_inflation_percentage(monthly_kpis):
    """Assert identity: duplicate_inflation_pct = duplicate_inflation / raw_recovery * 100."""
    for idx, row in monthly_kpis.iterrows():
        raw = row["raw_recovery_inr"]
        dup = row["duplicate_inflation_inr"]
        pct = row["duplicate_inflation_pct"]
        
        if raw > 0:
            expected_pct = (dup / raw) * 100
            diff = abs(expected_pct - pct)
            assert diff < 0.01, f"Inflation percentage mismatch for month {row['month']}: expected {expected_pct:.2f}%, got {pct:.2f}%"

def test_feb_mar_growth_reproducibility(monthly_kpis):
    """Assert Feb-Mar MoM clean growth calculation (+11.81%)."""
    feb = monthly_kpis[monthly_kpis["month"] == "2026-02"]["clean_recovery_inr"].values[0]
    mar = monthly_kpis[monthly_kpis["month"] == "2026-03"]["clean_recovery_inr"].values[0]
    
    clean_growth = ((mar - feb) / feb) * 100
    assert abs(clean_growth - 11.81) < 0.1, f"Expected Feb-Mar growth ~11.81%, got {clean_growth:.2f}%"
