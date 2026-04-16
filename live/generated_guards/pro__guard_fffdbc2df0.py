def guard(features: dict, prediction: str) -> str:
    # Reject longs when macd_histogram is negative (bearish momentum)
    if prediction == "long" and features.get("macd_histogram", 0) < 0:
        return "skip"
    # Reject shorts when macd_histogram is positive (bullish momentum)
    if prediction == "short" and features.get("macd_histogram", 0) > 0:
        return "skip"
    return prediction