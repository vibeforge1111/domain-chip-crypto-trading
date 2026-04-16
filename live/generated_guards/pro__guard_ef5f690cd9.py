def guard(features: dict, prediction: str) -> str:
    """Skip trades when macd_histogram contradicts the predicted direction."""
    macd = features.get("macd_histogram", 0)
    if prediction == "long" and macd < -0.0001:
        return "skip"
    if prediction == "short" and macd > 0.0001:
        return "skip"
    return prediction