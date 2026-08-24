# Production Analytics System Architecture: Collections Data Platform

## System Overview & Implementation Scope
This architecture document outlines both the **currently implemented local analytics pipeline** and the **proposed enterprise production scale-up architecture**.

---

## SECTION A: CURRENTLY IMPLEMENTED ARCHITECTURE (Assignment Implementation)

```text
+-----------------------------------------------------------------------------------+
|                  CURRENT LOCAL PIPELINE IMPLEMENTATION (BUILT)                     |
+-----------------------------------------------------------------------------------+
|  1. RAW DATA           | 17 Relational CSV Datasets in data/raw/                 |
|         │              | (Accounts, Payments, Calls, Dispositions, Agents)        |
|         ▼              |                                                          |
|  2. ETL ENGINE         | Python 3.11 / Pandas Data Cleaning & Entity Resolution    |
|         │              | (src/build_golden.py)                                    |
|         ▼              |                                                          |
|  3. GOLDEN DATASET     | Account-Month Aggregated Layer (210,000 rows)             |
|         │              | (outputs/golden_account_month.csv)                       |
|         ▼              |                                                          |
|  4. SQL METRICS LAYER  | DuckDB / ANSI Analytical Views & Transformation Queries  |
|         │              | (sql/01_cleaning.sql & sql/02_metrics.sql)               |
|         ▼              |                                                          |
|  5. TESTING & QUALITY  | Pytest Automated Unit Test Suite                         |
|         │              | (tests/test_payments.py, test_golden.py, test_metrics.py)|
|         ▼              |                                                          |
|  6. PRESENTATION LAYER | Streamlit Executive Dashboard & Jupyter Notebook         |
|                        | (dashboard/dashboard.py & notebook/collections_analysis.ipynb)|
+-----------------------------------------------------------------------------------+
```

---

## SECTION B: PROPOSED ENTERPRISE SCALE-UP ARCHITECTURE (Not Implemented in Assignment)

```text
+-----------------------------------------------------------------------------------+
|             PROPOSED ENTERPRISE PRODUCTION ARCHITECTURE (FUTURE SCALE-UP)         |
+-----------------------------------------------------------------------------------+
|  OPERATIONAL DATABASES  | OLTP Databases, Telephony CDPs, Payment Webhook Gateways|
|         │               |                                                         |
|         ▼               |                                                         |
|  INGESTION & STORAGE    | Kafka Event Streams / Amazon S3 Data Lake               |
|         │               |                                                         |
|         ▼               |                                                         |
|  DATA WAREHOUSE         | Snowflake / Google BigQuery / AWS Redshift              |
|         │               |                                                         |
|         ▼               |                                                         |
|  TRANSFORMATION         | dbt (data build tool) Incremental Models                |
|         │               |                                                         |
|         ▼               |                                                         |
|  DATA QUALITY           | Great Expectations / Soda Core Quality Quarantine Rules |
|         │               |                                                         |
|         ▼               |                                                         |
|  FEATURE STORE          | Feast / Hopsworks ML Feature Store                      |
|         │               |                                                         |
|         ▼               |                                                         |
|  TARGETING ENGINE       | Real-time XGBoost / Dynamic Channel Dispatch API        |
+-----------------------------------------------------------------------------------+
```

> 📌 **Note on Scope**: Section A represents the fully working, tested Python/SQL pipeline delivered in this repository. Section B outlines proposed future architectural enhancements for multi-region cloud deployment.

---

## Data Contracts & Primary Keys (Current Implementation)

1. **`payments` Table**:
   * **Primary Key**: `payment_id`
   * **Natural Key**: `payment_reference`
   * **Deduplication Constraint**: `payment_status = 'SUCCESS'`, deduplicated on `payment_reference` keeping earliest timestamp.
2. **`agents` Table**:
   * **Primary Key**: `agent_id`
   * **Entity Resolution**: Partitioned by `agent_id`, ordered by `updated_at DESC` to retain active agent record.
3. **`golden_account_month` Table**:
   * **Composite Primary Key**: `(account_id, month)`
   * **Granularity**: Exactly 1 row per active account per month (210,000 rows across 30,000 accounts for 7 complete months).
