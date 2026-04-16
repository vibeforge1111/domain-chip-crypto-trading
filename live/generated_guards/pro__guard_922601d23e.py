def guard(features: dict, prediction: str) -> str:
    """Skip trades against the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    # Reject longs when broader trend is bearish (rsi_2h < 40)
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    # Reject shorts when broader trend is bullish (rsi_2h > 60)
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    return prediction