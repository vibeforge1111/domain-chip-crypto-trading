def guard(features: dict, prediction: str) -> str:
    """Skip false compressions where volatility hasn't truly contracted."""
    # False compression: high bb_width with high atr_ratio
    if features["bb_width"] > 0.12 and features["atr_ratio"] > 1.1:
        return "skip"
    # Stochastic extremes indicate exhausted moves
    if prediction == "long" and features["stoch_k"] > 85:
        return "skip"
    if prediction == "short" and features["stoch_k"] < 15:
        return "skip"
    return prediction