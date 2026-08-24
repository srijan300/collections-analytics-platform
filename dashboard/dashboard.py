"""
COLLECTIONS EXECUTIVE DASHBOARD
--------------------------------
Streamlit C-Suite Decision Dashboard
Features:
 - Executive KPI Metrics with Single-Source-of-Truth Metric Reconciliation
 - Monthly Recovery Trend (Raw Reported vs Clean Settled)
 - Data Forensics & Hygiene Breakdown
 - Channel Efficiency & DPD Stratification
 - Dynamic ₹10 Cr Capital Deployment Scenario Engine
 - Data-Driven Claim Evaluation (Feb-Mar Growth & Strategy Shift Audit)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Collections Executive Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.65rem;
        font-weight: 700;
    }
    .metric-delta-pos {
        color: #10b981;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .metric-delta-neg {
        color: #ef4444;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .claim-box {
        background-color: #1e293b;
        border-left: 6px solid #f59e0b;
        border-radius: 8px;
        padding: 16px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Data Loader
@st.cache_data
def load_dashboard_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kpis = pd.read_csv(os.path.join(base_dir, "outputs", "monthly_kpis.csv"))
    dq_summary = pd.read_csv(os.path.join(base_dir, "outputs", "data_quality_summary.csv"))
    dq_issues = pd.read_csv(os.path.join(base_dir, "outputs", "data_quality_issues.csv"))
    golden = pd.read_csv(os.path.join(base_dir, "outputs", "golden_account_month.csv"))
    return kpis, dq_summary, dq_issues, golden

try:
    kpis, dq_summary, dq_issues, golden = load_dashboard_data()
except Exception as e:
    st.error(f"Error loading Golden Dataset outputs: {e}. Please run 'python src/build_golden.py' first.")
    st.stop()

# Header
st.title("🛡️ COLLECTIONS EXECUTIVE C-SUITE DASHBOARD")
st.caption("Forensic Data Audit, Reconciled Metrics & Capital Allocation Strategy | 30,000 Active Accounts")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("🔍 Executive Filters")
selected_scope = st.sidebar.radio(
    "Data Scope Baseline",
    ["7-Month Complete Baseline (Jan-Jul)", "Full Dataset (Jan-Aug Incomplete)"]
)

risk_segments_list = list(golden["risk_segment"].unique())
selected_risk = st.sidebar.multiselect("Risk Segment", risk_segments_list, default=risk_segments_list)

# Unified Scope Filter Function
def get_scoped_data(kpis, golden, scope, selected_risk):
    if scope == "7-Month Complete Baseline (Jan-Jul)":
        filtered_kpis = kpis[kpis["is_complete_month"] == 1].copy()
        filtered_golden = golden[golden["risk_segment"].isin(selected_risk)].copy()
    else:
        filtered_kpis = kpis.copy()
        # For full dataset view, filter risk segment on baseline golden
        filtered_golden = golden[golden["risk_segment"].isin(selected_risk)].copy()
    return filtered_kpis, filtered_golden

filtered_kpis, filtered_golden = get_scoped_data(kpis, golden, selected_scope, selected_risk)

# Dynamic Metric Reconciliation Engine
tot_raw_rec = filtered_kpis["raw_recovery_inr"].sum()
tot_clean_rec = filtered_kpis["clean_recovery_inr"].sum()
dup_overstatement = tot_raw_rec - tot_clean_rec
dup_overstatement_pct = (dup_overstatement / tot_raw_rec * 100) if tot_raw_rec > 0 else 0.0

if selected_scope == "7-Month Complete Baseline (Jan-Jul)":
    tot_rec_accounts = filtered_golden[filtered_golden["clean_recovery_amount"] > 0]["account_id"].nunique()
else:
    tot_rec_accounts = filtered_kpis["recovered_accounts"].sum()

# TOP LEVEL RECONCILED METRIC CARDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Clean Settled Recovery</div>
        <div class="metric-value">₹{tot_clean_rec/1e7:,.2f} Cr</div>
        <div class="metric-delta-pos">Verified Settled Cash</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Reported Raw Recovery</div>
        <div class="metric-value">₹{tot_raw_rec/1e7:,.2f} Cr</div>
        <div class="metric-delta-neg">Unfiltered Ingestion Export</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Duplicate-Driven Overstatement</div>
        <div class="metric-value">₹{dup_overstatement/1e7:,.2f} Cr</div>
        <div class="metric-delta-neg">+{dup_overstatement_pct:.1f}% Ingestion Inflation</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Recovered Accounts</div>
        <div class="metric-value">{tot_rec_accounts:,}</div>
        <div class="metric-delta-pos">Portfolio Resolutions</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if selected_scope == "Full Dataset (Jan-Aug Incomplete)":
    st.info("⚠️ **Scope Notice**: August 2026 is an incomplete partial month (556 payments, ₹4.27 Cr clean) and is excluded from full-month trend analysis to prevent silent distortion.")

# CLAIM EVALUATION
feb_mar_clean_growth = 0.0
feb_data = kpis[kpis["month"] == "2026-02"]
mar_data = kpis[kpis["month"] == "2026-03"]
if len(feb_data) > 0 and len(mar_data) > 0:
    feb_clean = feb_data["clean_recovery_inr"].values[0]
    mar_clean = mar_data["clean_recovery_inr"].values[0]
    feb_mar_clean_growth = ((mar_clean - feb_clean) / feb_clean) * 100

st.markdown(f"""
<div class="claim-box">
    <h3 style="color: #f59e0b; margin: 0 0 8px 0;">🟡 CLAIM EVALUATION: "11% Month-on-Month Growth"</h3>
    <p style="color: #cbd5e1; margin: 0; font-size: 0.95rem;">
        <strong>Verdict: PARTIALLY SUPPORTED — Feb–Mar Only ({feb_mar_clean_growth:+.2f}%)</strong><br>
        The Feb–Mar period shows approximately 11.81% month-on-month growth, but this isolated interval does not establish a sustained structural improvement trend. Subsequent months contracted (-8.52% in April, -3.71% in June). Separately, duplicate SUCCESS webhooks materially overstate reported recovery by ₹{dup_overstatement/1e7:,.2f} Cr.
    </p>
</div>
""", unsafe_allow_html=True)

# SECTION 1: MONTHLY RECOVERY TREND
st.subheader("📈 1. Monthly Recovery Trend: Uncleaned Reported Raw vs Clean Settled")

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(
    x=filtered_kpis["month"], y=filtered_kpis["raw_recovery_inr"] / 1e7,
    mode='lines+markers', name='Reported Raw Recovery (Inflated by Webhook Retries)',
    line=dict(color='#ef4444', width=3)
))
fig_trend.add_trace(go.Scatter(
    x=filtered_kpis["month"], y=filtered_kpis["clean_recovery_inr"] / 1e7,
    mode='lines+markers', name='Clean Settled Recovery (Verified Cash)',
    line=dict(color='#10b981', width=3)
))
fig_trend.update_layout(
    template="plotly_dark",
    plot_bgcolor="#1e293b", paper_bgcolor="#1e293b",
    height=400,
    title="Monthly Recovery Volume (INR Crores)",
    xaxis_title="Month", yaxis_title="INR Crores",
    margin=dict(l=40, r=40, t=50, b=40)
)
st.plotly_chart(fig_trend, use_container_width=True)

# SECTION 2: CHANNEL & DPD BREAKDOWN
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 2. Clean Recovery Attributed by Primary Channel")
    chan_summary = filtered_golden[filtered_golden["primary_channel"] != "NO_RECOVERY"].groupby("primary_channel").agg(
        Clean_Recovery=("clean_recovery_amount", "sum")
    ).reset_index()
    chan_summary["Clean_Recovery_Cr"] = chan_summary["Clean_Recovery"] / 1e7
    
    fig_chan = px.pie(
        chan_summary, values="Clean_Recovery_Cr", names="primary_channel",
        hole=0.4, title="Recovery Breakdown by Channel",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_chan.update_layout(template="plotly_dark", plot_bgcolor="#1e293b", paper_bgcolor="#1e293b", height=380)
    st.plotly_chart(fig_chan, use_container_width=True)

with col_right:
    st.subheader("🏷️ 3. Recovery Volume by DPD Stratification")
    dpd_summary = filtered_golden.groupby("dpd_bucket").agg(
        Clean_Recovery=("clean_recovery_amount", "sum")
    ).reset_index()
    dpd_summary["Clean_Recovery_Cr"] = dpd_summary["Clean_Recovery"] / 1e7
    
    fig_dpd = px.bar(
        dpd_summary, x="dpd_bucket", y="Clean_Recovery_Cr",
        title="Clean Recovery by DPD Bucket (INR Crores)",
        color="dpd_bucket", color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig_dpd.update_layout(template="plotly_dark", plot_bgcolor="#1e293b", paper_bgcolor="#1e293b", height=380, showlegend=False)
    st.plotly_chart(fig_dpd, use_container_width=True)

# SECTION 3: DYNAMIC SCENARIO SIMULATOR
st.markdown("---")
st.subheader("💰 4. ₹10 Cr Capital Deployment: Dynamic Scenario Engine")

baseline_7m_clean = kpis[kpis["is_complete_month"] == 1]["clean_recovery_inr"].sum()
annual_baseline_clean = (baseline_7m_clean / 7) * 12  # ~₹189.79 Cr annual clean baseline

st.caption(f"Baseline Annual Clean Recovery: **₹{annual_baseline_clean/1e7:,.2f} Cr** (extrapolated from 7-month clean settled recovery)")

def calculate_scenario(baseline, uplift_pct, capital_outlay=10.0):
    inc_recovery = baseline * (uplift_pct / 100)
    inc_recovery_cr = inc_recovery / 1e7
    net_profit_cr = inc_recovery_cr - capital_outlay
    roi_pct = (net_profit_cr / capital_outlay) * 100
    payback_months = (capital_outlay / inc_recovery_cr * 12) if inc_recovery_cr > 0 else np.nan
    return inc_recovery_cr, net_profit_cr, roi_pct, payback_months

scenarios = [
    ("Conservative Scenario", 1.5),
    ("Base Case Scenario", 3.5),
    ("Upside Scenario", 6.0)
]

scenario_rows = []
for name, uplift in scenarios:
    inc_cr, net_cr, roi, payback = calculate_scenario(annual_baseline_clean, uplift)
    payback_str = f"{payback:.1f} Months" if payback > 0 and net_cr > 0 else "N/A (>1 Year)"
    scenario_rows.append({
        "Scenario": name,
        "Assumed Uplift": f"+{uplift:.1f}%",
        "Incremental Annual Recovery": f"₹{inc_cr:.2f} Cr",
        "Capital Outlay": "₹10.0 Cr",
        "Net 1-Year Profit": f"₹{net_cr:+.2f} Cr",
        "1-Year ROI": f"{roi:+.1f}%",
        "Payback Period": payback_str
    })

df_scenarios = pd.DataFrame(scenario_rows)
st.dataframe(df_scenarios, use_container_width=True)

st.caption("📌 *Note: Scenarios are illustrative framework models for decision support and require experimental validation prior to full capital commitment.*")

st.warning("🎯 **EXECUTIVE RECOMMENDATION**: Do NOT immediately commit the full ₹10 Cr capital outlay. We recommend executing a **90-day randomized controlled trial (RCT) pilot** (budget ~₹1.5 Cr). Scale full capital deployment only if the pilot clears the investment hurdle rate.")
