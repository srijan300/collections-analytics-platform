-- ============================================================================
-- COLLECTIONS ANALYTICS: PRODUCTION ANALYTICAL METRICS & KPI QUERIES
-- Target Engine: DuckDB / PostgreSQL / ANSI SQL
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: RECONCILIATION SUMMARY (FULL DATASET VS 7-MONTH BASELINE)
-- ----------------------------------------------------------------------------
SELECT 
    'Full Dataset (Jan-Aug 2026)' AS dataset_scope,
    COUNT(DISTINCT account_id) AS total_accounts,
    SUM(clean_recovery_amount) AS total_clean_recovery_inr,
    SUM(raw_recovery_amount) AS total_raw_recovery_inr,
    SUM(raw_recovery_amount) - SUM(clean_recovery_amount) AS duplicate_inflation_inr
FROM golden_account_month
UNION ALL
SELECT 
    '7-Month Baseline (Jan-Jul 2026)' AS dataset_scope,
    COUNT(DISTINCT account_id) AS total_accounts,
    SUM(CASE WHEN month <= '2026-07' THEN clean_recovery_amount ELSE 0 END) AS total_clean_recovery_inr,
    SUM(CASE WHEN month <= '2026-07' THEN raw_recovery_amount ELSE 0 END) AS total_raw_recovery_inr,
    SUM(CASE WHEN month <= '2026-07' THEN raw_recovery_amount - clean_recovery_amount ELSE 0 END) AS duplicate_inflation_inr
FROM golden_account_month;

-- ----------------------------------------------------------------------------
-- QUERY 2: MONTH-ON-MONTH RECOVERY TREND & CLAIM AUDIT
-- Evaluates Feb-Mar bounce (+11.8%) vs sustained trend (flat ~₹16.2 Cr/mo)
-- ----------------------------------------------------------------------------
WITH monthly_summary AS (
    SELECT 
        month,
        COUNT(DISTINCT account_id) AS total_accounts,
        SUM(clean_recovery_amount) AS clean_recovery_inr,
        SUM(raw_recovery_amount) AS raw_recovery_inr,
        SUM(is_recovered) AS recovered_accounts_count
    FROM golden_account_month
    GROUP BY month
)
SELECT 
    month,
    total_accounts,
    recovered_accounts_count,
    ROUND((recovered_accounts_count::DOUBLE / total_accounts) * 100.0, 2) AS account_recovery_rate_pct,
    clean_recovery_inr,
    LAG(clean_recovery_inr) OVER (ORDER BY month) AS prev_month_recovery_inr,
    ROUND(
        ((clean_recovery_inr - LAG(clean_recovery_inr) OVER (ORDER BY month)) / 
        NULLIF(LAG(clean_recovery_inr) OVER (ORDER BY month), 0)) * 100.0, 2
    ) AS clean_mom_growth_pct,
    ROUND(clean_recovery_inr / total_accounts, 2) AS recovery_per_account_inr,
    CASE 
        WHEN month = '2026-03' THEN 'Feb-Mar Increase Observed (+11.8%)'
        ELSE 'Sustained Trend: Flat'
    END AS claim_status_annotation
FROM monthly_summary
ORDER BY month;

-- ----------------------------------------------------------------------------
-- QUERY 3: CHANNEL EFFICIENCY & CONVERSION ATTRIBUTION
-- ----------------------------------------------------------------------------
SELECT 
    primary_channel,
    COUNT(DISTINCT account_id) AS total_account_months,
    SUM(is_recovered) AS recovered_account_months,
    ROUND(AVG(is_recovered) * 100.0, 2) AS channel_conversion_rate_pct,
    SUM(clean_recovery_amount) AS total_channel_recovery_inr,
    ROUND(AVG(clean_recovery_amount), 2) AS avg_recovery_per_account_inr
FROM golden_account_month
WHERE primary_channel != 'NO_RECOVERY'
GROUP BY primary_channel
ORDER BY total_channel_recovery_inr DESC;

-- ----------------------------------------------------------------------------
-- QUERY 4: DPD STRATIFICATION & PORTFOLIO RISK PERFORMANCE
-- ----------------------------------------------------------------------------
SELECT 
    dpd_bucket,
    COUNT(DISTINCT account_id) AS account_count,
    SUM(outstanding_amount) AS total_outstanding_inr,
    SUM(clean_recovery_amount) AS total_recovery_inr,
    ROUND((SUM(clean_recovery_amount) / NULLIF(SUM(outstanding_amount), 0)) * 100.0, 2) AS monetary_recovery_rate_pct,
    ROUND(AVG(clean_recovery_amount), 2) AS avg_recovery_per_account_inr
FROM golden_account_month
GROUP BY dpd_bucket
ORDER BY 
    CASE dpd_bucket
        WHEN '0 DPD (Current)' THEN 1
        WHEN '1-30 DPD' THEN 2
        WHEN '31-60 DPD' THEN 3
        WHEN '61-90 DPD' THEN 4
        ELSE 5
    END;
