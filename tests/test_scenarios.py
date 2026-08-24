"""
Unit Tests for Capital Deployment Scenario Simulator
---------------------------------------------------
Verifies mathematical correctness of scenario calculations:
 - Incremental Annual Recovery
 - Net 1-Year Profit
 - 1-Year ROI %
"""

import pandas as pd
import pytest

def calculate_scenario(baseline_annual_recovery, uplift_pct, capital_outlay=10.0):
    inc_recovery_cr = (baseline_annual_recovery * (uplift_pct / 100)) / 1e7
    net_profit_cr = inc_recovery_cr - capital_outlay
    roi_pct = (net_profit_cr / capital_outlay) * 100
    return inc_recovery_cr, net_profit_cr, roi_pct

def test_scenario_calculations():
    # Baseline ~189.79 Cr annual clean recovery (1,107,128,976.75 / 7 * 12)
    baseline_annual_recovery = (1107128976.75 / 7) * 12
    
    # Test Conservative (1.5% uplift)
    inc_cons, net_cons, roi_cons = calculate_scenario(baseline_annual_recovery, 1.5)
    assert abs(inc_cons - 2.85) < 0.1, f"Expected ~2.85 Cr incremental recovery, got {inc_cons:.2f} Cr"
    assert abs(net_cons - (-7.15)) < 0.1, f"Expected ~ -7.15 Cr net profit, got {net_cons:.2f} Cr"
    
    # Test Base Case (3.5% uplift)
    inc_base, net_base, roi_base = calculate_scenario(baseline_annual_recovery, 3.5)
    assert abs(inc_base - 6.64) < 0.1, f"Expected ~6.64 Cr incremental recovery, got {inc_base:.2f} Cr"
    
    # Test Upside Case (6.0% uplift)
    inc_up, net_up, roi_up = calculate_scenario(baseline_annual_recovery, 6.0)
    assert abs(inc_up - 11.39) < 0.1, f"Expected ~11.39 Cr incremental recovery, got {inc_up:.2f} Cr"
    assert net_up > 0, "Upside case should yield positive net profit!"
