import numpy as np
import pandas as pd


HF_FEATURE_COLUMNS = [
    "revolving_utilization_pct",
    "age",
    "late_30_59",
    "debt_ratio",
    "income",
    "open_loans",
    "late_90",
    "real_estate_loans",
    "late_60_89",
    "dependents",
    "log_income",
    "weighted_late_score",
    "disposable_income",
    "log_debt_ratio",
]

MODEL_FEATURE_COLUMNS = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberRealEstateLoansOrLines",
    "NumberOfDependents",
    "WeightedLateScore",
    "LogIncome",
    "DisposableIncome",
    "LogDebtRatio",
]

DISPLAY_LABELS = {
    "revolving_utilization_pct": "Revolving Utilization",
    "age": "Age",
    "late_30_59": "Late 30-59 Days",
    "debt_ratio": "Debt Ratio",
    "income": "Monthly Income",
    "open_loans": "Open Credit Lines and Loans",
    "late_90": "Late 90 Days",
    "real_estate_loans": "Real Estate Loans",
    "late_60_89": "Late 60-89 Days",
    "dependents": "Dependents",
    "log_income": "Log Income",
    "weighted_late_score": "Weighted Late Score",
    "disposable_income": "Disposable Income",
    "log_debt_ratio": "Log Debt Ratio",
}


def build_feature_frame(
    *,
    age,
    revolving_utilization_pct,
    debt_ratio,
    income,
    open_loans,
    real_estate_loans,
    dependents,
    late_30_59,
    late_60_89,
    late_90,
):
    record = {
        "revolving_utilization_pct": float(revolving_utilization_pct),
        "age": int(age),
        "late_30_59": int(late_30_59),
        "debt_ratio": float(debt_ratio),
        "income": float(income),
        "open_loans": int(open_loans),
        "late_90": int(late_90),
        "real_estate_loans": int(real_estate_loans),
        "late_60_89": int(late_60_89),
        "dependents": float(dependents),
    }
    record["log_income"] = float(np.log1p(record["income"]))
    record["weighted_late_score"] = (
        record["late_30_59"] * 1
        + record["late_60_89"] * 2
        + record["late_90"] * 4
    )
    record["disposable_income"] = float(record["income"] * (1 - record["debt_ratio"]))
    record["log_debt_ratio"] = float(np.log1p(record["debt_ratio"]))

    return pd.DataFrame([record], columns=HF_FEATURE_COLUMNS)


def build_model_feature_frame(features):
    row = features.iloc[0]
    model_record = {
        "RevolvingUtilizationOfUnsecuredLines": float(row["revolving_utilization_pct"]),
        "age": int(row["age"]),
        "NumberOfOpenCreditLinesAndLoans": int(row["open_loans"]),
        "NumberRealEstateLoansOrLines": int(row["real_estate_loans"]),
        "NumberOfDependents": float(row["dependents"]),
        "WeightedLateScore": float(row["weighted_late_score"]),
        "LogIncome": float(row["log_income"]),
        "DisposableIncome": float(row["disposable_income"]),
        "LogDebtRatio": float(row["log_debt_ratio"]),
    }
    return pd.DataFrame([model_record], columns=MODEL_FEATURE_COLUMNS)


def build_display_frame(features):
    display_frame = features.copy()
    return display_frame.rename(columns=DISPLAY_LABELS)
