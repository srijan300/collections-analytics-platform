# Assumptions & Metric Definitions: Collections Analytics Framework

## Overview
Existing collections metrics often rely on flawed assumptions—such as treating any answered call as a meaningful contact or evaluating recovery growth without deduplicating payment retries. This document establishes rigorous, production-grade metric definitions for the platform.

---

## Metric Definitions & Business Justification

### 1. Contact Rate (%)
* **Standardized Definition**:
  $$\text{Contact Rate} = \frac{\text{Calls with Duration} \ge 15 \text{ seconds AND Call Status} = \text{'ANSWERED'}}{\text{Total Unique Call Attempts}}$$
* **Reasoning**: A call under 15 seconds rarely represents a meaningful conversation with a borrower. Filtering noise isolates genuine customer engagements.

### 2. Right-Party Contact (RPC) Rate (%)
* **Standardized Definition**:
  $$\text{RPC Rate} = \frac{\text{Calls resulting in Disposition} \in \{\text{'PTP'}, \text{'PAID'}, \text{'CALLBACK'}, \text{'REFUSED'}, \text{'DISPUTE'}\}}{\text{Total Answered Calls}}$$
* **Analytical Nuance**: **RPC is approximated using validated borrower-relevant dispositions because an explicit right-party indicator column is absent in raw telephony logs.** This prevents overcounting non-borrower respondents or wrong numbers.

### 3. Account Recovery Rate (%) vs Monetary Recovery Rate (%)
To prevent confusion between portfolio account coverage and financial cash realization, we maintain two distinct recovery rates:

* **Account Recovery Rate (%)**:
  $$\text{Account Recovery Rate} = \frac{\text{Distinct Accounts with Clean SUCCESS Payment in Month}}{\text{Total Active Accounts in Portfolio}}$$
  * *Purpose*: Evaluates portfolio resolution depth across accounts.

* **Monetary Recovery Rate (%)**:
  $$\text{Monetary Recovery Rate} = \frac{\text{Total Clean Deduplicated Recovery Amount (INR)}}{\text{Total Portfolio Outstanding Principal Balance (INR)}}$$
  * *Purpose*: Evaluates total financial cash recovery against outstanding exposure.

### 4. PTP Kept Rate (%)
* **Standardized Definition**:
  $$\text{PTP Kept Rate} = \frac{\text{PTPs with Status} = \text{'KEPT' (Matching Payment within 7 days AND Amount} \ge \text{Promised Amount)}}{\text{Total Promised PTPs}}$$
* **Reasoning**: Assesses the true financial quality of promises secured by agents. Promises without subsequent payment verification or partial payments below the promised threshold are categorized as broken.

### 5. Recovery per Account (₹)
* **Standardized Definition**:
  $$\text{Recovery per Account} = \frac{\text{Total Clean Deduplicated Recovery Amount (INR)}}{\text{Total Active Accounts}}$$
* **Reasoning**: Provides a normalized unit economic metric for revenue generation across portfolio segments.

### 6. Cost per ₹ Recovered (₹/₹)
* **Standardized Definition**:
  $$\text{Cost per ₹ Recovered} = \frac{\text{Total Channel Operating Expense (Telephony + Agent Salary + Field Expenses)}}{\text{Total Clean Recovery (INR)}}$$
* **Reasoning**: Essential financial metric for capital allocation. Field visits have high cost per rupee recovered (~₹0.18/₹), whereas WhatsApp digital engagement operates at low cost (~₹0.02/₹).
