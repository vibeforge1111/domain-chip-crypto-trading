def guard(features: dict, prediction: str) -> str:
    """Skip entries when MACD histogram shows momentum deceleration."""
    macd_hist = features.get("macd_histogram", 0)
    # For longs: skip if MACD histogram is negative (momentum weakening)
    if prediction == "long" and macd_hist < -0.0001:
        return "skip"
    # For shorts: skip if MACD histogram is positive (momentum weakening)
    if prediction == "short" and macd_hist > 0.0001:
        return "skip"
    return prediction