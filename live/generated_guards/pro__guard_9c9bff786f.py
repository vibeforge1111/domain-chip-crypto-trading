def guard(features: dict, prediction: str) -> str:
    """Skip entries when MACD histogram shows momentum deceleration."""
    macd_histogram = features.get('macd_histogram', 0)
    
    # For longs: skip if histogram is barely positive (bullish momentum decelerating)
    if prediction == "long" and 0 < macd_histogram < 0.0008:
        return "skip"
    
    # For shorts: skip if histogram is barely negative (bearish momentum weakening)
    if prediction == "short" and -0.0008 < macd_histogram < 0:
        return "skip"
    
    return prediction