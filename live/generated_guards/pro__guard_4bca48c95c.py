def guard(features: dict, prediction: str) -> str:
    # Filter longs when macd_histogram is bearish (momentum against direction)
    if prediction == "long" and features.get("macd_histogram", 0) < -0.0002:
        return "skip"
    # Filter shorts when macd_histogram is bullish (momentum against direction)
    if prediction == "short" and features.get("macd_histogram", 0) > 0.0002:
        return "skip"
    # Skip longs when stoch_k is overbought (momentum exhaustion risk)
    if prediction == "long" and features.get("stoch_k", 50) > 85:
        return "skip"
    # Skip shorts when stoch_k is oversold (bounce risk)
    if prediction == "short" and features.get("stoch_k", 50) < 15:
        return "skip"
    return prediction