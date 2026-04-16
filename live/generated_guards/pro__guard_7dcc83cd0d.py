def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum deceleration against direction."""
    macd = features.get("macd_histogram", 0)
    # Long trades fail when MACD histogram is negative (bearish momentum)
    if prediction == "long" and macd < 0:
        return "skip"
    # Short trades fail when MACD histogram is positive (bullish momentum)
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction