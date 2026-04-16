def guard(features: dict, prediction: str) -> str:
    """Skip trades where momentum is decelerating against the direction."""
    macd_hist = features.get("macd_histogram", 0)
    if prediction == "long" and macd_hist < -0.0001:
        return "skip"
    if prediction == "short" and macd_hist > 0.0001:
        return "skip"
    return prediction