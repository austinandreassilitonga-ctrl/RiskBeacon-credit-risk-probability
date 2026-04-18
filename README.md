# RiskBeacon — Automated Credit Risk Probability Pipeline with Predictive Analytics and Real-Time Monitoring

> **Minimizing losses from loan defaults, while ensuring creditworthy members still receive the access they deserve.**

![logo](img/logo.png).

---

## Table of Contents

- [About the Project](#about-the-project)
- [Business Background](#business-background)
- [Objectives](#objectives)
- [Dataset](#dataset)
- [System Architecture](#system-architecture)
- [Pipeline Overview](#pipeline-overview)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Modeling](#modeling)
- [Business Impact Simulation](#business-impact-simulation)
- [Credit Decision Logic](#credit-decision-logic)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Team](#team)
- [References](#references)

---

## About the Project

**RiskBeacon** is a credit risk scoring system designed to assess and monitor the probability of borrower default before a credit decision is made.

RiskBeacon transforms historical borrower data into **objective, data-driven credit decisions** through an integrated analysis and modeling pipeline grounded in the universally recognized **5C of Credit** principles — Character, Capacity, Capital, Collateral, and Conditions.

The system is built to serve both **banking institutions** and **cooperative lenders (Koperasi Simpan Pinjam)**, bridging the gap between informal trust-based lending and modern predictive analytics.

### System Components

| Component | Description |
|---|---|
| **Data Pipeline & Quality Monitoring** | Ingestion, transformation, and validation of historical borrower data — handling missing values, outliers, and class imbalance |
| **Exploratory Data Analysis** | Business insights into borrower behavior mapped across the 5C framework |
| **Predictive Modeling** | LightGBM classification model to estimate Probability of Default (PD) at the individual borrower level |
| **Model Explainability** | SHAP-based feature attribution to explain each borrower's risk score |
| **Operational Risk Monitoring** | Risk segmentation into three tiers — Low, Medium, and High — based on PD score distribution |

---

## Business Background

As financial institutions — from banks to cooperative lenders — continue to expand their reach, subjective credit assessment remains a critical operational risk. Over-reliance on social reputation and informal judgment can lead to:

- Increasing Non-Performing Loans (NPL)
- Inconsistent and biased credit decisions
- Financial losses from defaults that could have been prevented

Particularly in the context of **Koperasi Simpan Pinjam**, the `Character` dimension of 5C credit assessment still heavily depends on social reputation — not data or numbers. This creates blind spots that RiskBeacon is specifically designed to address.

> *"Before RiskBeacon was applied, an actual default rate of 6.7% across 150,000 borrowers was not detectable at the individual level. After the predictive model was applied to a separate dataset of 100,000 borrowers, RiskBeacon identified 28.5% of applicants as showing default indicators — surfacing hidden risk that would previously have been approved without scrutiny."*

---

## Objectives

1. Build an end-to-end automated pipeline from raw Excel data to credit risk scoring
2. Represent the **5C of Credit** framework through data features and model design
3. Generate a **Probability of Default (PD) Score** for each borrower
4. Segment borrowers into **Low / Medium / High Risk** tiers
5. Provide credit limit recommendations based on risk tier
6. Minimize NPL while maintaining credit access for creditworthy members

---

## Dataset

| Property | Detail |
|---|---|
| Source | [Give Me Some Credit — Kaggle](https://www.kaggle.com/datasets/brycecf/give-me-some-credit-dataset) |
| Origin | Credit Fusion competition, Kaggle 2011 |
| Training rows | 150,000 |
| Total features | 11 columns |
| Target variable | `SeriousDlqin2yrs` (1 = default, 0 = no default) |
| Class imbalance | ~6.7% default rate |

### Feature Mapping to 5C of Credit

| Feature | 5C Dimension | Business Meaning |
|---|---|---|
| `SeriousDlqin2yrs` | — | Target: default within 2 years |
| `RevolvingUtilizationOfUnsecuredLines` | Capacity | % of credit limit used |
| `Age` | Character | Borrower age — proxy for credit history length |
| `NumberOfTime30-59DaysPastDueNotWorse` | Character | Early warning: 30–59 day late payments |
| `DebtRatio` | Capacity | Total monthly debt / monthly income |
| `MonthlyIncome` | Capacity | Primary repayment capacity indicator |
| `NumberOfOpenCreditLinesAndLoans` | Capital | Total active credit obligations |
| `NumberOfTimes90DaysLate` | Character | Strongest signal: 90+ day delinquency history |
| `NumberRealEstateLoansOrLines` | Collateral | Property-backed credit — reduces risk |
| `NumberOfTime60-89DaysPastDueNotWorse` | Character | Intermediate delinquency signal |
| `NumberOfDependents` | Capital | Financial burden from dependents |

---

## System Architecture

```
Excel Data (Cooperative)
        │
        ▼
   Upload to Storage
        │
        ▼
┌─────────────────────────────┐
│   Apache Airflow DAG        │
│  ┌─────────────────────┐    │
│  │ Extract             │    │
│  │ Schema Validation   │    │
│  │ Transform           │    │
│  │ Load to Database    │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
        │
        ▼
   Exploratory Data Analysis
   (WoE + IV Feature Selection)
        │
        ▼
┌─────────────────────────────┐
│   LightGBM Model            │
│  Train / Test Split 80:20   │
│  Hyperparameter Tuning      │
│  Evaluation: AUC, Recall,   │
│  KS-Statistic, SHAP         │
└─────────────────────────────┘
        │
        ▼
   PD Score per Borrower (0.0 – 1.0)
        │
   ┌────┴────────┬────────────┐
   ▼             ▼            ▼
Low Risk     Medium Risk   High Risk
High Limit   Mod. Limit    Rejected
```

---

## Pipeline Overview

### ETL — Apache Airflow

| Stage | Process |
|---|---|
| **Extract** | Read Excel file → parse to DataFrame |
| **Validate** | Check schema, data types, duplicates — send error notification to admin if invalid |
| **Transform** | Missing value imputation, outlier handling, encoding, feature engineering |
| **Load** | Save clean data to database / data lake |

### Analysis & Modeling

| Stage | Process |
|---|---|
| **EDA** | Distribution analysis, correlation heatmap, class imbalance check |
| **Feature Selection** | Weight of Evidence (WoE) + Information Value (IV) |
| **Modeling** | LightGBM with imbalance handling (SMOTE / class weight) |
| **Evaluation** | ROC-AUC, Recall, KS-Statistic, SHAP explainability |

---

## Exploratory Data Analysis

Key findings from EDA:

- **Class imbalance**: 93.3% non-default vs 6.7% default — requires SMOTE or class weighting
- **Strongest predictors**: `NumberOfTimes90DaysLate`, `RevolvingUtilizationOfUnsecuredLines`, `NumberOfTime30-59DaysPastDueNotWorse`
- **DebtRatio** has significant outliers requiring IQR-based capping
- **MonthlyIncome** has ~20% missing values — imputed using grouped median

---

## Modeling

### Model: LightGBM

LightGBM was selected for its strong performance on imbalanced tabular data, built-in handling of missing values, and fast training speed that suits a production pipeline deployment.

### Evaluation Metrics

| Metric | Purpose in Credit Context |
|---|---|
| **ROC-AUC** | Overall discrimination power of the model |
| **Recall** | Priority metric — minimize missed defaults (False Negatives = direct financial loss) |
| **KS-Statistic** | Industry-standard banking metric — maximum separation between default and non-default distributions |
| **SHAP** | Explainability — justify individual credit decisions to loan officers and regulators |

> **Why Recall over Precision?**
> In credit risk, a False Negative (predicting safe when the borrower will actually default) directly erodes the institution's capital. A False Positive (rejecting a safe borrower) is a missed opportunity — painful but not catastrophic. Recall is therefore the primary optimization target.

### Model Performance Results

| Metric | Score |
|---|---|
| **ROC-AUC** | 0.92 |
| **Recall** | 0.74 |
| **KS-Statistic** | 0.58 |

### KS-Statistic Interpretation

| KS Value | Model Quality |
|---|---|
| < 0.20 | Very weak — rebuild |
| 0.20 – 0.40 | Acceptable |
| 0.40 – 0.60 | Good — production ready |
| 0.60 – 0.75 | Very good |
| > 0.75 | Excellent — validate for overfitting |

---

## Business Impact Simulation

| | Before (Baseline) | After (Model Applied) |
|---|---|---|
| Population | 150,000 borrowers | 100,000 borrowers |
| Default rate | 6.7% (actual) | 28.5% (predicted) |
| Interpretation | True distribution in training data | Model surfaces hidden risk in unseen population |

> *Before: actual default distribution from training data (n=150,000). After: model prediction results on an unseen borrower population (n=100,000). The elevated predicted default rate reflects the model's ability to identify risk patterns that are invisible through manual assessment.*

---

## Credit Decision Logic

PD Score thresholds are determined from the KS-Statistic optimal cut-off point and the percentile distribution of PD scores in the training data.

| Risk Segment | PD Score | Credit Decision | Limit |
|---|---|---|---|
| 🟢 **Low Risk** | < 0.43 | Approved | High limit — standard interest rate |
| 🟡 **Medium Risk** | 0.43 – 0.53 | Approved with review | Moderate limit — manual officer review required |
| 🔴 **High Risk** | ≥ 0.53 | Rejected | No credit — financial literacy referral |

> Note: Thresholds are calibrated based on the portfolio default rate (~6.7%) and the KS-Statistic optimal separation point. They are not fixed constants — recalibration is recommended when applied to a new borrower population.

---

## Project Structure

```
├── Business Understanding/            # Business Overview and Flowchart
├── Data Analyst/                      # Exploratory Data Analysis and Business Insight
├── Data Engineer/                     # Apache Airflow DAG files
├── Data Scientist/                    # Modeling and Evaluations
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Orchestration** | Apache Airflow |
| **Data Processing** | Python, Pandas, NumPy |
| **Feature Engineering** | Scikit-learn, Weight of Evidence (custom) |
| **Modeling** | LightGBM |
| **Explainability** | SHAP |
| **Imbalance Handling** | Imbalanced-learn (SMOTE) |
| **Evaluation** | Scikit-learn metrics, KS-Statistic |
| **Storage** | PostgreSQL / CSV |
| **Visualization** | Matplotlib, Seaborn |
| **Version Control** | Git, GitHub |

---

## Team

| Name | Role |
|---|---|
| Austin Silitonga | Lead Project — Business Understanding |
| Hernanda Rifaldi | Data Engineer — ETL Pipeline & Airflow |
| Kesyia Patty | Data Analyst — EDA & Business Insight |
| M.Nabil | Data Scientist — Feature Engineering & Modeling |
| Rezha Aulia | Data Scientist — SHAP & KS-Statistic |

---
## References

- Give Me Some Credit Dataset — [Kaggle](https://www.kaggle.com/datasets/brycecf/give-me-some-credit-dataset)
- Credit Fusion & Will Cukierski. *Give Me Some Credit*. Kaggle Competition, 2011.
- Basel II/III IRB Approach — Bank for International Settlements
- OJK POJK No.40/POJK.03/2019 — Asset Quality of Commercial Banks
- Siddiqi, N. (2006). *Credit Risk Scorecards*. Wiley.
- SHAP: Lundberg & Lee (2017). *A Unified Approach to Interpreting Model Predictions*.

---

<p align="center">
  Built with purpose — to make credit fairer, more objective, and data-driven.<br>
  <strong>RiskBeacon</strong> · FTDS Batch 037 · Hacktiv8 · 2025
</p>
