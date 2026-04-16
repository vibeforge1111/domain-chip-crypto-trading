def guard(features: dict, prediction: str) -> str:
    """Filter trades at extreme overbought/oversold conditions using BB and Stochastic."""
    if prediction == "long" and features["bb_pct_b"] > 0.9 and features["stoch_k"] > 80:
        return "skip"
    if prediction == "short" and features["bb_pct_b"] < 0.1 and features["stoch_k"] < 20:
        return "skip"
    return prediction