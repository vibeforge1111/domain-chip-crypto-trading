def guard(features: dict, prediction: str) -> str:
    # Reject longs when MACD histogram is negative (momentum deceleration)
    if prediction == "long" and features.get("macd_histogram", 0) < -0.0001:
        return "skip"
    # Reject shorts when MACD histogram is positive (momentum acceleration)
    if prediction == "short" and features.get("macd_histogram", 0) > 0.0001:
        return "skip"
    return prediction