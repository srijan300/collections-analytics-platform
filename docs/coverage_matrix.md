# Assignment Requirement Coverage Matrix

This document tracks all formal requirements for the Collections Analytics & Data Forensics assignment, detailing their implementation, file location, evidence, and verification status.

---

| Requirement | Implementation Details | Evidence / File Location | Status |
| :--- | :--- | :--- | :---: |
| **1. Raw Data Ingestion** | Ingested all 17 relational CSV datasets from `data/raw/` using pandas with schema validation. | `src/build_golden.py` (`load_data()`) | ✅ VERIFIED |
| **2. Data Profiling & Audit** | Profiled records, schemas, timestamp formats, primary key nulls, and duplicate records. | `docs/data_quality_report.md`, `outputs/data_quality_summary.csv` | ✅ VERIFIED |
| **3. Payment Deduplication** | Filtered `SUCCESS` payments and deduplicated gateway retries on `payment_reference`. | `src/build_golden.py` (`clean_payments()`), `tests/test_payments.py` | ✅ VERIFIED |
| **4. Entity Resolution** | Deduplicated `agents.csv` snapshot updates using `updated_at` ordering to resolve active profiles. | `src/build_golden.py` (`clean_agents()`), `sql/01_cleaning.sql` | ✅ VERIFIED |
| **5. Timezone Standardisation** | Standardized timestamps across telephony, sessions, and payments to UTC/IST normalization. | `src/build_golden.py`, `sql/01_cleaning.sql` | ✅ VERIFIED |
| **6. Golden Dataset (210k Rows)** | Built account-month grid: 30,000 active accounts x 7 complete baseline months (Jan-Jul 2026) = 210,000 rows. | `src/build_golden.py`, `outputs/golden_account_month.csv` | ✅ VERIFIED |
| **7. Single Composite Grain** | Enforced exact composite primary key `(account_id, month)` uniqueness constraint. | `tests/test_golden.py` (`test_golden_grain_uniqueness`) | ✅ VERIFIED |
| **8. Production SQL Metrics** | Created DuckDB SQL cleaning views and monthly KPI metric queries matching Python logic. | `sql/01_cleaning.sql`, `sql/02_metrics.sql` | ✅ VERIFIED |
| **9. Reconciled Monthly Recovery** | Reconciled raw reported SUCCESS recovery (₹129.29 Cr) vs clean settled recovery (₹110.71 Cr). | `outputs/monthly_kpis.csv`, `dashboard/dashboard.py` | ✅ VERIFIED |
| **10. Audit of "11% Growth Claim"** | Evaluated claim: Feb-Mar showed +11.81% bounce, but April dropped -8.52%. Verdict: PARTIALLY SUPPORTED. | `docs/executive_memo.md`, `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **11. DPD Stratification** | Stratified portfolio recovery across 0 DPD, 1-30 DPD, 31-60 DPD, 61-90 DPD, and 90+ DPD (NPA). | `notebook/collections_analysis.ipynb`, `dashboard/dashboard.py` | ✅ VERIFIED |
| **12. Portfolio Mix Analysis** | Analyzed recovery distribution by loan type (Personal, Business, Auto, Microfinance). | `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **13. Geographic Analysis** | Analyzed recovery by state/city from borrower demographics. | `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **14. Agent Tenure Analysis** | Evaluated agent tenure (<3m, 3-6m, 6-12m, >12m) against PTP Kept Rate and recovery output. | `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **15. Telephony & Calling Time** | Analyzed answered call rates by hour of day and telephony vendor performance. | `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **16. Attempt Frequency Audit** | Measured diminishing marginal return and complaint risk of calling >4 times/day. | `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **17. Channel Attribution** | Attributed clean recovery across Voice Call, WhatsApp, SMS, Field Visit, and Digital Direct. | `dashboard/dashboard.py`, `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **18. Statistical / Causal Audit** | Audited campaign strategy shift (v1 vs v3) via observational Diff-in-Diff; documented non-significance (p=0.14). | `docs/executive_memo.md`, `notebook/collections_analysis.ipynb` | ✅ VERIFIED |
| **19. ₹10 Cr Capital Deployment** | Evaluated Option 4 (ML Dynamic Targeting) under Conservative (1.5%), Base (3.5%), and Upside (6.0%) scenarios. | `docs/executive_memo.md`, `dashboard/dashboard.py` | ✅ VERIFIED |
| **20. Controlled Pilot Recommendation**| Recommended 90-day randomized pilot (~₹1.5 Cr) before full capital deployment. | `docs/executive_memo.md`, `README.md` | ✅ VERIFIED |
| **21. Executive Dashboard** | Implemented interactive Streamlit C-Suite dashboard with single filter scope and dynamic metrics. | `dashboard/dashboard.py` | ✅ VERIFIED |
| **22. Automated Pytest Suite** | Developed automated test suite covering schema, deduplication, grain, non-negativity, and math identity. | `tests/test_payments.py`, `tests/test_golden.py`, `tests/test_metrics.py` | ✅ VERIFIED |
| **23. Executive Memorandum** | Authored professional board memo with reconciliation table, claim verdict, and pilot recommendation. | `docs/executive_memo.md` | ✅ VERIFIED |
| **24. Metric Definitions Framework**| Authored standardized definitions for Contact Rate, RPC Rate, Recovery Rate, and PTP Kept Rate. | `docs/assumptions_and_metric_definitions.md` | ✅ VERIFIED |
| **25. Architecture Specification**| Documented Section A (Current Local Implementation) vs Section B (Proposed Future Scale-Up). | `docs/architecture.md`, `docs/architecture.png` | ✅ VERIFIED |
| **26. Reproducibility & Cleanliness**| Verified 100% reproducible execution from fresh environment; removed junk/scratch files. | `README.md`, `requirements.txt` | ✅ VERIFIED |
