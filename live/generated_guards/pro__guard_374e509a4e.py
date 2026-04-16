def guard(features: dict, prediction: str) -> str:
    """Reject trades when macd_histogram shows momentum misalignment."""
    macd = features.get('macd_histogram', 0)
    # Long trades need bullish momentum; reject if histogram is negative
    if prediction == "long" and macd < -0.0005:
        return "skip"
    # Short trades need bearish momentum; reject if histogram is positive
    if prediction == "short" and macd > 0.0005:
        return "skip"
    return prediction