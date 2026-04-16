def guard(features: dict, prediction: str) -> str:
    # Skip longs when both Stoch K > 80 and BB %B > 0.85 (overbought extreme)
    if prediction == "long" and features["stoch_k"] > 80 and features["bb_pct_b"] > 0.85:
        return "skip"
    # Skip shorts when both Stoch K < 20 and BB %B < 0.15 (oversold extreme)
    if prediction == "short" and features["stoch_k"] < 20 and features["bb_pct_b"] < 0.15:
        return "skip"
    return prediction