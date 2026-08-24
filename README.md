# Collections Analytics & Data Forensics Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Production_SQL-orange.svg)](https://duckdb.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b.svg)](https://streamlit.io/)
[![Pytest](https://img.shields.io/badge/Pytest-Automated_Tests-green.svg)](https://docs.pytest.org/)

## Executive Overview
This repository delivers an end-to-end, production-grade analytics platform, data forensics audit, and decision-support system for a **₹114.99 Cr Collections Portfolio (30,000 active accounts)** across 17 relational raw datasets.

### Single Source of Truth Reconciliation

| Metric Scope | Raw Reported SUCCESS | Clean Settled Recovery | Webhook Retry Inflation | Inflation % | Baseline Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Full Ingestion Dataset**<br>*(Jan – Aug 2026)* | **₹134.15 Cr**<br>*(17,880 rows)* | **₹114.99 Cr**<br>*(15,350 rows)* | **₹19.16 Cr**<br>*(2,530 duplicates)* | **16.66%** | Complete database extract up to August 2026. |
| **7-Month Complete Baseline**<br>*(Jan – Jul 2026)* | **₹129.29 Cr**<br>*(16,368 rows)* | **₹110.71 Cr**<br>*(14,094 rows)* | **₹18.58 Cr**<br>*(2,274 duplicates)* | **16.78%** | **Primary Comparable Baseline**. August is excluded from full-month MoM trends as an incomplete partial month (only ₹4.27 Cr logged). |

---

## Claim Evaluation & Causal Findings

1. **"11% Month-on-Month Growth Claim"** 🟡 **PARTIALLY SUPPORTED (Feb–Mar Only)**
   - The data supports an approximately 11% increase for the specific Feb–Mar period (**+11.81%**), but does **NOT** support a sustained, structural month-on-month improvement trend. Clean recovery remains structurally flat (**~₹16.0 Cr – ₹16.5 Cr clean/mo**).
2. **Strategy Shift Causality** 🔴 **INSUFFICIENT STATISTICAL EVIDENCE**
   - DiD observational regression estimates strategy shift uplift at **+1.2% (p = 0.14)**. The effect is **not statistically significant**.
3. **₹10 Cr Capital Deployment Recommendation** 🎯 **RANDOMIZED PILOT FIRST**
   - Do **NOT** commit ₹10 Cr upfront. Deploy a **90-day randomized controlled trial (RCT) pilot (budget ₹1.5 Cr)** for ML targeting. Scale full capital deployment only if incremental recovery clears the investment hurdle rate.

---

## ⚡ Quickstart & Reproducibility Command

Run the entire pipeline from scratch in 4 simple commands:

```bash
# 1. Activate Environment & Install Dependencies
.venv\Scripts\activate
pip install -r requirements.txt

# 2. Build Analytical Golden Dataset (210,000 rows)
python src/build_golden.py

# 3. Run Automated Unit Test Suite
python -m pytest tests/

# 4. Launch Executive Streamlit Dashboard
streamlit run dashboard/dashboard.py
```

---

## 📂 Repository Structure

```text
collections_assignment_solution/
├── data/
│   └── raw/                                # 17 Relational raw CSV files
├── src/
│   └── build_golden.py                     # Python ETL pipeline with entity resolution & deduplication
├── sql/
│   ├── 01_cleaning.sql                     # Production DuckDB cleaning & deduplication views
│   └── 02_metrics.sql                      # Analytical KPI queries & MoM reconciliation
├── outputs/
│   ├── golden_account_month.csv            # 210,000 row analytical layer (Jan-Jul complete baseline)
│   ├── monthly_kpis.csv                    # Reconciled monthly KPI table
│   ├── data_quality_summary.csv            # Executive data quality summary
│   └── data_quality_issues.csv             # Forensic audit logs (DQ-001 to DQ-005)
├── tests/
│   ├── test_payments.py                    # Unit tests for payment deduplication & status filters
│   ├── test_golden.py                      # Unit tests for Golden Dataset schema & grain constraints
│   └── test_metrics.py                     # Unit tests for monthly KPI math reconciliation
├── notebook/
│   └── collections_analysis.ipynb          # Pre-executed Jupyter Notebook with pre-rendered visual outputs
├── dashboard/
│   └── dashboard.py                        # Streamlit C-Suite Executive Dashboard
├── docs/
│   ├── executive_memo.md                   # Executive C-Suite Memorandum
│   ├── data_quality_report.md              # Forensic Data Hygiene & Quality Audit Report
│   ├── assumptions_and_metric_definitions.md # Standardized Metric Definitions Framework
│   ├── architecture.md                     # System Architecture Specification
│   └── architecture.png                    # System Architecture Diagram
├── requirements.txt                        # Project dependencies
└── README.md                               # Project documentation
```

---

## System Architecture

```text
SECTION A: CURRENTLY IMPLEMENTED PIPELINE (Built & Tested)
----------------------------------------------------------------------------------
Raw CSV Data (data/raw/) ──► Python/Pandas Deduplication (src/build_golden.py) 
  ──► Golden Account-Month Layer (outputs/golden_account_month.csv) 
  ──► DuckDB SQL Layer (sql/) ──► Pytest Suite (tests/) 
  ──► Streamlit Dashboard (dashboard/dashboard.py) & Notebook (notebook/)

SECTION B: PROPOSED ENTERPRISE SCALE-UP (Future Infrastructure - Not Implemented)
----------------------------------------------------------------------------------
Kafka Event Streams / S3 Data Lake ──► Snowflake Data Warehouse 
  ──► dbt Transformations & Great Expectations ──► Feast ML Feature Store 
  ──► Real-time XGBoost Targeting Engine ──► Automated Dialer CRM Integration
```
