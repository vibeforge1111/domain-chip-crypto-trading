def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram indicates momentum deceleration."""
    macd = features.get("macd_histogram", 0)
    # For longs, require positive momentum; skip if decelerating (negative histogram)
    if prediction == "long" and macd < 0:
        return "skip"
    # For shorts, require negative momentum; skip if decelerating (positive histogram)
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction