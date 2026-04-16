def guard(features: dict, prediction: str) -> str:
    # Skip longs when overbought: price near upper BB AND stochastic overbought
    if prediction == "long" and features.get("bb_pct_b", 0) > 0.85 and features.get("stoch_k", 0) > 80:
        return "skip"
    # Skip shorts when oversold: price near lower BB AND stochastic oversold
    if prediction == "short" and features.get("bb_pct_b", 0) < 0.15 and features.get("stoch_k", 0) < 20:
        return "skip"
    return prediction