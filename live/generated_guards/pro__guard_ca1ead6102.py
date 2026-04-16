def guard(features: dict, prediction: str) -> str:
    """Reject trades when macd_histogram shows momentum against direction."""
    macd = features.get("macd_histogram", 0)
    # Skip longs when momentum is bearish
    if prediction == "long" and macd < 0:
        return "skip"
    # Skip shorts when momentum is bullish
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction