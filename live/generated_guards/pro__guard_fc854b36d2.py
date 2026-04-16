def guard(features: dict, prediction: str) -> str:
    """Skip entries when MACD histogram shows momentum deceleration."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip long if histogram is positive but near zero (bullish momentum decelerating)
    if prediction == "long" and 0 < macd_hist < 0.0003:
        return "skip"
    
    # Skip short if histogram is negative but near zero (bearish momentum decelerating)
    if prediction == "short" and -0.0003 < macd_hist < 0:
        return "skip"
    
    return prediction