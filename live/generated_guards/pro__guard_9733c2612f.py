def guard(features: dict, prediction: str) -> str:
    # Skip longs when overbought: BB at upper band AND stochastic overbought
    if prediction == "long" and features["bb_pct_b"] > 0.85 and features["stoch_k"] > 80:
        return "skip"
    # Skip shorts when oversold: BB at lower band AND stochastic oversold
    if prediction == "short" and features["bb_pct_b"] < 0.15 and features["stoch_k"] < 20:
        return "skip"
    return prediction