# EXECUTIVE MEMORANDUM: COLLECTIONS PERFORMANCE & CAPITAL ALLOCATION

**TO:** Executive Leadership & Board of Directors  
**FROM:** Lead Data Analyst & Forensics Team  
**DATE:** August 24, 2026  
**SUBJECT:** Collections Performance Audit, Forensic Reconciliation & Capital Allocation Strategy  

---

## Executive Summary & Claim Status

| Evaluated Claim | Forensic Audit Verdict | Supporting Evidence |
| :--- | :--- | :--- |
| **"11% Month-on-Month Growth Claim"** | 🟡 **PARTIALLY SUPPORTED**<br>*(Feb–Mar Only, Not Sustained)* | Feb $\rightarrow$ Mar recovery grew **+11.81%** (approx 11%). However, April dropped **-8.52%**, and June dropped **-3.71%**. Clean recovery is structurally flat across full months (**~₹15.8 Cr – ₹16.7 Cr clean/mo**). |
| **"Causal Strategy Shift Uplift"** | 🔴 **INSUFFICIENT STATISTICAL EVIDENCE** | Estimated strategy shift uplift = **+1.2% (p = 0.14)**. At $\alpha = 0.05$, the effect is **not statistically significant**. |
| **"₹10 Cr Investment Recommendation"** | 🎯 **SCENARIO PILOT FIRST** | Do NOT commit ₹10 Cr upfront. Deploy a **90-day randomized pilot** for ML targeting. Scale only if incremental recovery exceeds the investment hurdle. |

---

## 1. Data Forensic Audit & Metric Reconciliation

### Single Source of Truth Reconciliation Table

```text
====================================================================================================
METRIC SCOPE                   RAW REPORTED (INR)      CLEAN SETTLED (INR)     DUPLICATE INFLATION
====================================================================================================
Full Ingestion Dataset (Jan-Aug)   ₹134.15 Cr             ₹114.99 Cr             ₹19.16 Cr (16.66%)
7-Month Baseline (Jan-Jul)        ₹129.29 Cr             ₹110.71 Cr             ₹18.58 Cr (16.78%)
Partial August 2026 (Excluded)     ₹4.86 Cr               ₹4.27 Cr               ₹0.58 Cr
====================================================================================================
```

* **Note on Scope**: The raw database contains payments up to August 2026 (₹114.99 Cr clean total). However, August is an incomplete partial month (only 556 payments logged). Therefore, **Jan–Jul 2026 (7 complete months, totaling ₹110.71 Cr clean recovery)** is established as the primary comparable baseline analysis window.

### Monthly Recovery Trend Breakdown (7 Complete Baseline Months)

| Month | Raw Reported (INR) | Clean Settled (INR) | Raw MoM (%) | Clean MoM (%) | Account Recovery Rate | Audit Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **2026-01** | ₹19.11 Cr | ₹16.38 Cr | -- | -- | 7.15% | Baseline |
| **2026-02** | ₹17.41 Cr | ₹14.91 Cr | -8.99% | -8.99% | 6.67% | Seasonal dip |
| **2026-03** | ₹19.32 Cr | ₹16.67 Cr | **+11.81%** | **+11.81%** | 7.45% | **Feb–Mar Bounce (Tax Refund Cycle)** |
| **2026-04** | ₹17.84 Cr | ₹15.25 Cr | -8.52% | -8.52% | 6.99% | Contraction |
| **2026-05** | ₹18.70 Cr | ₹15.96 Cr | +4.62% | +4.62% | 7.12% | Stable |
| **2026-06** | ₹17.87 Cr | ₹15.36 Cr | -3.71% | -3.71% | 6.90% | Stable |
| **2026-07** | ₹19.03 Cr | ₹16.18 Cr | +5.27% | +5.27% | 7.04% | Stable |
| **TOTAL** | **₹129.29 Cr** | **₹110.71 Cr** | -- | -- | **7.05% Avg** | **Flat (~₹16.0–16.5 Cr/mo)** |

---

## 2. Analytical Findings & Driver Analysis

1. **The 11% Claim Refinement**: The data supports an approximately 11% increase from February to March (+11.81%), but does **not** support a sustained 11% month-on-month improvement trend.
2. **Duplicate Ingestion Inflation**: Gateway webhook retry mechanics logged 2,274 duplicate `SUCCESS` records in Jan–Jul, inflating raw reports by **₹18.58 Cr**.
3. **Statistical Validity of Mid-Year Strategy Shift**: The estimated uplift of the campaign strategy shift (v1 vs v3) is **+1.2%, but it is not statistically significant (p = 0.14)**. Therefore, we do not have sufficient evidence to attribute observed changes to the strategy change.

---

## 3. ₹10 Cr Capital Deployment: Scenario-Based Modeling

Rather than relying on single deterministic forecasts, we model capital allocation under conservative, base, and upside operational scenarios over the baseline annual clean recovery of **₹196.8 Cr (₹16.4 Cr/mo $\times$ 12)**:

### Scenario Analysis: Option 4 — Better Borrower Targeting (ML Dynamic Contact Engine)

| Scenario | Assumed Recovery Uplift | Incremental Annual Recovery | Capital Cost | Net 1-Year Profit | Payback Period |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Conservative** | **+1.5%** | **₹2.95 Cr** | ₹10.0 Cr | -₹7.05 Cr | N/A |
| **Base Case** | **+3.5%** | **₹6.89 Cr** | ₹10.0 Cr | -₹3.11 Cr | 17.4 Mos |
| **Upside Case** | **+6.0%** | **₹11.81 Cr** | ₹10.0 Cr | **+₹1.81 Cr** | 10.2 Mos |

### CEO Takeaway & Investment Decision

> 🚨 **RECOMMENDED ACTION**: **The ₹10 Cr investment should NOT be committed all at once.**
>
> We recommend running a **90-day randomized controlled trial (RCT) pilot** in one regional zone with a budget of **₹1.5 Cr**. Scale full capital deployment only if incremental recovery clears the investment hurdle rate during the pilot phase.

---

## 4. Analyst Limitations

1. **Observational Data**: The dataset is observational and does not establish causal attribution for channel interventions.
2. **Incomplete August Data**: August 2026 data contains only partial-month records and is excluded from full-month comparisons.
3. **Right-Party Contact Approximation**: Telephony logs lack an explicit RPC flag; RPC is approximated using validated borrower dispositions.
4. **Local Prototype Architecture**: Production cloud integration (Kafka/Snowflake) is proposed as a scale-up design, not implemented in this local pipeline assignment.
