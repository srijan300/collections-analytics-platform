# Data Quality & Forensics Audit Report

## Executive Summary & Data Reconciliation
During the forensic audit of the collections dataset (covering 30,000 accounts across 17 relational tables), several critical data hygiene issues were detected. Uncleaned production reporting led to artificial revenue inflation, incorrect attribution, and distorted operational performance metrics.

### Single Source of Truth Reconciliation Table

| Metric Scope | Total Raw Reported SUCCESS | Total Clean Settled Recovery | Webhook Retry Inflation | Inflation % | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Full Ingestion Dataset**<br>*(Jan – Aug 2026)* | **₹134.15 Cr**<br>*(17,880 rows)* | **₹114.99 Cr**<br>*(15,350 rows)* | **₹19.16 Cr**<br>*(2,530 duplicates)* | **16.66%** | Contains all payment webhooks logged up to August 2026. |
| **7-Month Analysis Baseline**<br>*(Jan – Jul 2026)* | **₹129.29 Cr**<br>*(16,368 rows)* | **₹110.71 Cr**<br>*(14,094 rows)* | **₹18.58 Cr**<br>*(2,274 duplicates)* | **16.78%** | **Primary Comparable Baseline**. August is excluded from full-month MoM trends as an incomplete partial month (only ₹4.27 Cr logged). |

---

## Data Lineage Pipeline

```text
raw_payments.csv (25,500 rows)
       │
       ├── Filter: payment_status = 'SUCCESS' (17,880 rows, ₹134.15 Cr)
       │
       ├── Deduplicate: payment_reference (15,350 rows, ₹114.99 Cr clean)
       │
       ├── Filter Complete Analysis Window: event_at between Jan-01 & Jul-31 (14,094 rows, ₹110.71 Cr)
       │
       └── Aggregate by account_id + month ──► golden_account_month (210,000 rows)
```

---

## Detailed Data Hygiene Issues & Audit Trail

| Issue Code | Category | Raw Affected Records | Clean / Retained Records | Financial / Metric Impact | Action Taken |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **DQ-001** | Payment Ingestion Retries | 17,880 | 15,350 | Removed **₹19.16 Cr** (Full) / **₹18.58 Cr** (Jan-Jul) fake recovery | Deduplicated on `payment_reference` retaining earliest event timestamp. |
| **DQ-002** | Non-SUCCESS Statuses | 7,620 | 0 | Excluded **₹57.58 Cr** in `REVERSED`, `PENDING`, and `FAILED` rows | Filtered ledger strictly to `payment_status = 'SUCCESS'`. |
| **DQ-003** | Agent Entity Duplication | 30,000 | 1,000 | Corrected agent capacity & productivity metrics | Window function `ROW_NUMBER() OVER (PARTITION BY agent_id ORDER BY updated_at DESC)`. |
| **DQ-004** | Disposition Code Inconsistency | 35,000 | 35,000 | Standardized PTP & Contact Rate baseline | Mapped `PROMISE_TO_PAY` -> `PTP`, `NO_ANSWER`/`BUSY` -> `NO_CONTACT`. |
| **DQ-005** | Timezone Variances | 91,350 | 91,350 | Fixed peak-hour call dialer attribution | Standardized mixed timezones (`UTC`, `Asia/Kolkata`, `Asia/Dubai`) to normalized UTC/IST. |
