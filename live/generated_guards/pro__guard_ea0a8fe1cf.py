def guard(features: dict, prediction: str) -> str:
    macd = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    # Skip longs when macd histogram is negative (bearish momentum)
    # and price is already below VWAP (confirming weakness)
    if prediction == "long" and macd < 0 and vwap_dev < 0:
        return "skip"
    # Skip shorts when macd histogram is positive (bullish momentum)
    # and price is already above VWAP (confirming strength)
    if prediction == "short" and macd > 0 and vwap_dev > 0:
        return "skip"
    return prediction