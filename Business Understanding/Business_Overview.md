# RiskBeacon
## Business Overview

### Project Overview

**RiskBeacon** is a credit scoring analysis and modeling system designed to help financial institutions — particularly cooperative lending organizations (Koperasi Simpan Pinjam) — assess credit worthiness more objectively and consistently. The system is built by representing the **5C of Credit** principles — **Character, Capacity, Capital, Collateral, and Conditions** — through a data-driven approach based on historical borrower records.

By utilizing quantitative variables such as income, debt ratio, and payment delinquency history, **RiskBeacon** is able to produce individual risk estimates in the form of a probability of default and a credit score that is easy for decision-makers to understand and act on.

The core problem that RiskBeacon aims to solve lies in the **Character** dimension, which in cooperative lending is still often assessed subjectively based on social reputation or personal familiarity. This approach can introduce bias and inconsistency in credit decisions, increasing the risk of misjudging members. RiskBeacon addresses this limitation by replacing subjective evaluation with data-based assessment, so that every decision is grounded in historical patterns and measurable risk indicators.

From a business perspective, RiskBeacon is designed to strike the right balance between reducing default risk and maximizing credit distribution to qualified borrowers. With clear risk segmentation (Low, Medium, High), cooperatives can implement more targeted credit strategies — such as adjusting credit limits or approval policies. The expected outcomes are an improvement in loan portfolio quality, a reduction in non-performing loans, and the creation of a more consistent, transparent, and sustainable credit decision system.

---

### Business Problem

Cooperative lending institutions frequently face **high default rates** that directly impact financial losses and disrupt cash flow. This problem is made worse by a credit approval process that lacks clear risk controls, which increases the likelihood of **bad debt**. There is also inconsistency in decision-making: members with similar financial conditions can receive different outcomes due to subjective assessments, especially when it comes to evaluating character.

At the same time, cooperatives face a **trade-off between risk and revenue**. An overly restrictive approach is safer but reduces revenue potential, while an aggressive approach increases credit disbursement but raises the risk of default. This dynamic is reflected in real-world cases, including members losing assets due to inability to repay small loans, non-performing loan crises in regional cooperatives, and extreme cases of inhumane debt collection practices.

Reference cases:
- [Member Loses Home After Borrowing Rp 20M from Cooperative (Kompas)](https://regional.kompas.com/read/2025/09/09/153304878/kehilangan-rumah-usai-pinjam-rp-20-juta-di-koperasi-demak-hadi-punya-satu#)
- [NPL at 87% of Total Assets (Tempo)](https://www.tempo.co/ekonomi/anggota-koperasi-melania-masih-berjuang-bongkar-dugaan-penggelapan-uang-rp-210-miliar-2064084)
- [Employee Detained for 5 Days Over Rp 19M Debt (Liputan 6)](https://www.youtube.com/watch?v=J2-U59WHvAY)

---

### Business Objective

The analysis and model we built represent the **5C of Credit** principles widely used in both banking and cooperative lending, using a historical data-based approach to increase objectivity in credit assessment.

Specifically, this project targets:
- Surfacing hidden default risk that would previously have gone undetected without a scoring system
- Improving estimated profit per loan through better risk-adjusted credit decisions
- Recommending an appropriate loan amount based on each member's historical data

---

### Business Impact Simulation (Conceptual)

**Scenario 1 — Without a Model**
- Total members: 150,000
- Estimated default rate: 6.7%
- Without a scoring system, almost all loan applications would be approved without individual risk assessment.

**Scenario 2 — With the Predictive Model**
- Total members: 100,000 (separate dataset)
- Predicted default rate: 28.5%
- On a different historical dataset, the model identified a significantly higher proportion of borrowers with default indicators. This does not mean defaults have increased — it means the model successfully surfaces hidden risk that would otherwise have been approved without scrutiny.

**Scenario 3 — With Scoring + Credit Limit Recommendation**
- **Low Risk**: High limit — `Limit = (1 - risk_probability) × income`
- **Medium Risk**: Moderate limit — `Limit = 10% × income`
- **High Risk**: Rejected

With this segmentation, risk is better controlled while revenue continues to flow from creditworthy borrowers.

---

### Success Metrics

Primary target: **Reject users with a predicted default probability above 80%**

Model evaluation results:
- **ROC-AUC**: 0.92
- **Recall**: 0.74
- **KS-Statistic**: 0.58

**Dataset source**: [Give Me Some Credit — Kaggle](https://www.kaggle.com/competitions/GiveMeSomeCredit/overview)
