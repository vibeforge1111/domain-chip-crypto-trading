def guard(features: dict, prediction: str) -> str:
    # Detect momentum deceleration using MACD histogram
    # Skip longs when MACD histogram is negative (momentum losing strength)
    if prediction == "long" and features.get("macd_histogram", 0) < 0:
        return "skip"
    # Skip shorts when MACD histogram is positive (momentum losing strength for shorts)
    if prediction == "short" and features.get("macd_histogram", 0) > 0:
        return "skip"
    return prediction