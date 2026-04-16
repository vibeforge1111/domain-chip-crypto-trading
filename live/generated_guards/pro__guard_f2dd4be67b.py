def guard(features: dict, prediction: str) -> str:
    # Skip longs when MACD histogram is negative (bearish momentum deceleration)
    if prediction == "long" and features.get("macd_histogram", 0) < 0:
        return "skip"
    # Skip shorts when MACD histogram is positive (bullish momentum deceleration)
    if prediction == "short" and features.get("macd_histogram", 0) > 0:
        return "skip"
    return prediction