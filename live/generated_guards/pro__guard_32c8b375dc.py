def guard(features: dict, prediction: str) -> str:
    """Filter trades at Bollinger Band and Stochastic extremes."""
    # Skip long signals when overbought (near upper BB + high stochastic)
    if prediction == "long" and features["bb_pct_b"] > 0.85 and features["stoch_k"] > 80:
        return "skip"
    # Skip short signals when oversold (near lower BB + low stochastic)
    if prediction == "short" and features["bb_pct_b"] < 0.15 and features["stoch_k"] < 20:
        return "skip"
    return prediction