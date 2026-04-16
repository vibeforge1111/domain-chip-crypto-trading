def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram indicates momentum deceleration."""
    hist = features.get("macd_histogram", 0)
    if prediction == "long" and hist < 0:
        return "skip"
    if prediction == "short" and hist > 0:
        return "skip"
    return prediction