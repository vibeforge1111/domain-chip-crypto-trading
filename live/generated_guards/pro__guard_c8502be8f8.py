def guard(features: dict, prediction: str) -> str:
    """Filter trades with RSI extremes + large opposing wicks (reversal pattern)."""
    if prediction == "long":
        if features['rsi_14'] > 70 and features['lower_wick_ratio'] > 0.5:
            return "skip"
    elif prediction == "short":
        if features['rsi_14'] < 30 and features['upper_wick_ratio'] > 0.5:
            return "skip"
    return prediction