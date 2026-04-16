def guard(features: dict, prediction: str) -> str:
    # Skip longs when both indicators confirm overbought extreme
    if prediction == "long" and features["bb_pct_b"] > 0.9 and features["stoch_k"] > 85:
        return "skip"
    # Skip shorts when both indicators confirm oversold extreme
    if prediction == "short" and features["bb_pct_b"] < 0.1 and features["stoch_k"] < 15:
        return "skip"
    return prediction