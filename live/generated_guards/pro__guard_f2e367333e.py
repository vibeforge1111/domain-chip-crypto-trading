def guard(features: dict, prediction: str) -> str:
    """Reject trades when macd_histogram contradicts direction (momentum deceleration)."""
    hist = features.get("macd_histogram", 0)
    if prediction == "long" and hist < -0.00005:
        return "skip"
    if prediction == "short" and hist > 0.00005:
        return "skip"
    return prediction