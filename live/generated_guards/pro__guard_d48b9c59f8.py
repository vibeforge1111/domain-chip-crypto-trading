def guard(features: dict, prediction: str) -> str:
    """Custom guard function using macd_histogram for momentum deceleration detection."""
    macd = features.get("macd_histogram", 0)
    # Skip longs when macd histogram is significantly negative (bullish momentum decelerating)
    if prediction == "long" and macd < -0.0001:
        return "skip"
    # Skip shorts when macd histogram is significantly positive (bearish momentum decelerating)
    if prediction == "short" and macd > 0.0001:
        return "skip"
    return prediction