def guard(features: dict, prediction: str) -> str:
    # Reject long entries when macd_histogram is negative (momentum decelerating)
    if prediction == "long" and features.get("macd_histogram", 0) < 0:
        return "skip"
    # Reject short entries when macd_histogram is positive (momentum accelerating up)
    if prediction == "short" and features.get("macd_histogram", 0) > 0:
        return "skip"
    return prediction