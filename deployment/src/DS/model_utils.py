import json
from pathlib import Path

import joblib
import numpy as np

try:
    from .feature_engineering import build_model_feature_frame
except ImportError:
    from feature_engineering import build_model_feature_frame


ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "best_lgbm.pkl"
PREPROCESSOR_PATH = ARTIFACT_DIR / "transformer.pkl"
METADATA_PATH = ARTIFACT_DIR / "metadata.json"
DEFAULT_THRESHOLD = 0.3
LOW_RISK_MAX = 0.438
MEDIUM_RISK_MAX = 0.535
DECLINE_THRESHOLD = 0.80


def _sigmoid(value):
    return 1.0 / (1.0 + np.exp(-value))


def _load_threshold():
    if METADATA_PATH.exists():
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        return float(metadata.get("final_threshold", DEFAULT_THRESHOLD))
    return DEFAULT_THRESHOLD


def _categorize_probability(probability):
    if probability >= MEDIUM_RISK_MAX:
        return "High Risk"
    if probability >= LOW_RISK_MAX:
        return "Medium Risk"
    return "Low Risk"


def _build_credit_policy(probability, income):
    no_risk_probability = max(0.0, 1.0 - probability)

    if probability > DECLINE_THRESHOLD:
        return {
            "borrowing_decision": "Not eligible for borrowing",
            "recommended_credit_limit": 0.0,
            "no_risk_probability": no_risk_probability,
            "policy_note": "Risk probability is above 80%, so no credit should be extended.",
            "formula": "Declined when risk probability > 80%",
        }

    if probability >= MEDIUM_RISK_MAX:
        return {
            "borrowing_decision": "Eligible with restricted limit",
            "recommended_credit_limit": float(income * 0.10),
            "no_risk_probability": no_risk_probability,
            "policy_note": "High-risk borrowers between 53.5% and 80% are capped at 10% of monthly income.",
            "formula": "Credit limit = 10% x income",
        }

    return {
        "borrowing_decision": "Eligible for borrowing",
        "recommended_credit_limit": float(no_risk_probability * income),
        "no_risk_probability": no_risk_probability,
        "policy_note": "For low and medium risk borrowers, the limit is based on no-risk probability multiplied by income.",
        "formula": "Credit limit = (1 - risk probability) x income",
    }


def _predict_with_fallback(features):
    row = features.iloc[0]
    linear_score = (
        -3.0
        + 1.2 * row["late_30_59"]
        + 1.8 * row["late_60_89"]
        + 2.4 * row["late_90"]
        + 0.9 * min(row["revolving_utilization_pct"], 2.5)
        + 0.15 * min(row["debt_ratio"], 10.0)
        - 0.18 * row["log_income"]
    )
    probability = float(_sigmoid(linear_score))
    threshold = _load_threshold()
    label = _categorize_probability(probability)
    credit_policy = _build_credit_policy(probability, float(row["income"]))
    return {
        "probability": probability,
        "label": label,
        "source": "fallback_rule_based",
        "threshold": threshold,
        "risk_bands": {
            "high_risk_min": MEDIUM_RISK_MAX,
            "medium_risk_min": LOW_RISK_MAX,
            "medium_risk_max": MEDIUM_RISK_MAX,
            "low_risk_max": LOW_RISK_MAX,
        },
        **credit_policy,
    }


def predict_risk(features):
    if not MODEL_PATH.exists():
        return _predict_with_fallback(features)

    model = joblib.load(MODEL_PATH)
    transformed = build_model_feature_frame(features)

    if PREPROCESSOR_PATH.exists():
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        transformed = preprocessor.transform(transformed)

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(transformed)[0][1])
    else:
        prediction = float(model.predict(transformed)[0])
        probability = max(0.0, min(1.0, prediction))

    threshold = _load_threshold()
    label = _categorize_probability(probability)
    credit_policy = _build_credit_policy(probability, float(features.iloc[0]["income"]))
    return {
        "probability": probability,
        "label": label,
        "source": "best_lgbm.pkl",
        "threshold": threshold,
        "risk_bands": {
            "high_risk_min": MEDIUM_RISK_MAX,
            "medium_risk_min": LOW_RISK_MAX,
            "medium_risk_max": MEDIUM_RISK_MAX,
            "low_risk_max": LOW_RISK_MAX,
        },
        **credit_policy,
    }
