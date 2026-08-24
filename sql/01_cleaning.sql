-- ============================================================================
-- COLLECTIONS ANALYTICS: PRODUCTION DATA CLEANING & TRANSFORMATION (SQL)
-- Target Engine: DuckDB / PostgreSQL / ANSI SQL
-- ============================================================================

-- ----------------------------------------------------------------------------
-- STEP 1: ENTITY RESOLUTION & AGENT DEDUPLICATION
-- Resolve latest record per agent_id using updated_at windowing
-- ----------------------------------------------------------------------------
CREATE OR REPLACE TABLE stg_clean_agents AS
WITH ranked_agents AS (
    SELECT 
        agent_id,
        employee_code,
        agent_name,
        vendor_id,
        team,
        status,
        joined_at,
        updated_at,
        ROW_NUMBER() OVER (
            PARTITION BY agent_id 
            ORDER BY COALESCE(TRY_CAST(updated_at AS TIMESTAMP), TRY_CAST(joined_at AS TIMESTAMP)) DESC
        ) AS rn
    FROM raw_agents
)
SELECT 
    agent_id,
    employee_code,
    agent_name,
    vendor_id,
    team,
    status,
    joined_at,
    updated_at
FROM ranked_agents
WHERE rn = 1;

-- ----------------------------------------------------------------------------
-- STEP 2: PAYMENT DEDUPLICATION & STATUS FILTERING
-- Remove duplicate webhook payment retries (same payment_reference)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE TABLE stg_clean_payments AS
WITH deduplicated_succ_payments AS (
    SELECT 
        payment_id,
        account_id,
        borrower_id,
        TRY_CAST(event_at AS TIMESTAMP) AS event_at,
        payment_reference,
        amount,
        payment_status,
        payment_method,
        provider_id,
        ROW_NUMBER() OVER (
            PARTITION BY payment_reference 
            ORDER BY TRY_CAST(event_at AS TIMESTAMP) ASC, payment_id ASC
        ) AS pmt_rn
    FROM raw_payments
    WHERE payment_status = 'SUCCESS'
)
SELECT 
    payment_id,
    account_id,
    borrower_id,
    event_at,
    payment_reference,
    amount,
    payment_status,
    payment_method,
    provider_id,
    DATE_TRUNC('month', event_at) AS pmt_month
FROM deduplicated_succ_payments
WHERE pmt_rn = 1;

-- ----------------------------------------------------------------------------
-- STEP 3: DISPOSITION CODE STANDARDIZATION & TIMEZONE NORMALIZATION
-- Normalize legacy codes (e.g., PROMISE_TO_PAY -> PTP)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE TABLE stg_clean_call_dispositions AS
SELECT 
    disposition_id,
    account_id,
    borrower_id,
    TRY_CAST(event_at AS TIMESTAMP) AS event_at,
    call_id,
    agent_id,
    disposition_code AS raw_disposition_code,
    CASE UPPER(disposition_code)
        WHEN 'PROMISE_TO_PAY' THEN 'PTP'
        WHEN 'NO_ANSWER' THEN 'NO_CONTACT'
        WHEN 'BUSY' THEN 'NO_CONTACT'
        WHEN 'NOT_REACHABLE' THEN 'NO_CONTACT'
        ELSE UPPER(disposition_code)
    END AS clean_disposition_code,
    disposition_version
FROM raw_call_dispositions;

-- ----------------------------------------------------------------------------
-- STEP 4: GOLDEN ACCOUNT-MONTH ANALYTICAL LAYER
-- Aggregate clean payments, interactions, and DPD buckets by account & month
-- ----------------------------------------------------------------------------
CREATE OR REPLACE TABLE golden_account_month AS
WITH month_grid AS (
    SELECT DISTINCT 
        a.account_id,
        m.month_start
    FROM raw_accounts a
    CROSS JOIN (
        SELECT DATE '2026-01-01' + INTERVAL (i) MONTH AS month_start
        FROM GENERATE_SERIES(0, 6) s(i)
    ) m
),
monthly_pmts AS (
    SELECT 
        account_id,
        DATE_TRUNC('month', event_at) AS month_start,
        SUM(amount) AS clean_recovery_amount,
        COUNT(payment_id) AS clean_payment_count
    FROM stg_clean_payments
    GROUP BY account_id, DATE_TRUNC('month', event_at)
),
monthly_calls AS (
    SELECT 
        account_id,
        DATE_TRUNC('month', TRY_CAST(event_at AS TIMESTAMP)) AS month_start,
        COUNT(call_id) AS total_calls,
        SUM(CASE WHEN call_status = 'ANSWERED' THEN 1 ELSE 0 END) AS answered_calls,
        SUM(duration_sec) AS total_call_duration_sec
    FROM raw_calls
    GROUP BY account_id, DATE_TRUNC('month', TRY_CAST(event_at AS TIMESTAMP))
)
SELECT 
    mg.account_id,
    STRFTIME(mg.month_start, '%Y-%m') AS month,
    acc.borrower_id,
    acc.loan_type,
    acc.risk_segment,
    acc.dpd,
    CASE 
        WHEN acc.dpd = 0 THEN '0 DPD (Current)'
        WHEN acc.dpd <= 30 THEN '1-30 DPD'
        WHEN acc.dpd <= 60 THEN '31-60 DPD'
        WHEN acc.dpd <= 90 THEN '61-90 DPD'
        ELSE '90+ DPD (NPA)'
    END AS dpd_bucket,
    acc.principal_amount,
    acc.outstanding_amount,
    COALESCE(p.clean_recovery_amount, 0.0) AS clean_recovery_amount,
    COALESCE(p.clean_payment_count, 0) AS clean_payment_count,
    CASE WHEN COALESCE(p.clean_recovery_amount, 0.0) > 0 THEN 1 ELSE 0 END AS is_recovered,
    COALESCE(c.total_calls, 0) AS total_calls,
    COALESCE(c.answered_calls, 0) AS answered_calls,
    COALESCE(c.total_call_duration_sec, 0) AS total_call_duration_sec
FROM month_grid mg
LEFT JOIN raw_accounts acc ON mg.account_id = acc.account_id
LEFT JOIN monthly_pmts p ON mg.account_id = p.account_id AND mg.month_start = p.month_start
LEFT JOIN monthly_calls c ON mg.account_id = c.account_id AND mg.month_start = c.month_start;
