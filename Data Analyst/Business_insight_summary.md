# Business Insight Summary
## Project: Credit Risk Analysis — RiskBeacon

---

### 1. Default Overview

This analysis identifies key patterns that differentiate **"Current"** (non-defaulting) borrowers from **"Default"** borrowers. Based on a dataset of 150,000 entries, we found that historical payment behavior and financial burden are statistically significant predictors of default.

**Key Finding:** Borrowers with anomalous data in their delinquency frequency — categorized as "Unknown" — show a notably high default rate (~60%). This confirms that data anomalies in borrower records often serve as a hidden risk indicator that goes unreported under normal assessment.

---

### 2. Risk Patterns & Business Insights

#### A. Behavioral Risk — The "Red Flags"

**Extreme Delay:**
Borrowers with a history of repeated late payments show a very strong correlation with default risk. Delinquency frequency above 6 times almost guarantees a future default, with risk reaching above 60%. This is the strongest individual predictor in the dataset.

**Utilization Stress:**
Borrowers who use their credit limit to near-full capacity (Very High Utilization) have a default risk that is approximately **3× higher than the average**. This pattern suggests these borrowers are relying on credit to cover day-to-day cash flow needs — a condition known as being **over-leveraged**.

---

#### B. Customer Profile & Capacity

**Age Profile:**
There is a clear inverse relationship between age and default risk. The youngest age group (under 30 years old) shows the highest risk profile at approximately **12% default rate**. This is likely because younger borrowers tend to have shorter credit histories and less financial stability.

**Financial Burden:**
Default risk tends to rise as the number of financial dependents increases. The highest risk point is observed for borrowers with **6 dependents**, suggesting that a heavier household financial burden significantly reduces a borrower's ability to keep up with loan payments.

**Income Capacity:**
Borrowers in the **"Low" income category** are more vulnerable compared to those with higher income. This reinforces the role of economic capacity as a key factor in determining repayment discipline and loan reliability.

---

### 3. Summary

The three most influential factors for predicting default in this dataset are:
1. **Payment behavior** — frequency of late payments (especially 90+ days)
2. **Credit utilization** — how much of the credit limit is being used
3. **Household burden** — number of financial dependents

These findings align with the **5C of Credit** framework used as the foundation of this project, particularly the **Character** (payment history) and **Capacity** (income vs. debt load) dimensions.
