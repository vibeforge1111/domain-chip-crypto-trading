def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration against the trade direction."""
    macd_hist = features.get("macd_histogram", 0)
    # Long trades: skip if MACD histogram is deeply negative (bearish momentum)
    if prediction == "long" and macd_hist < -0.0003:
        return "skip"
    # Short trades: skip if MACD histogram is deeply positive (bullish momentum)
    if prediction == "short" and macd_hist > 0.0003:
        return "skip"
    return prediction