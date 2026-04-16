def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram indicates momentum deceleration."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip longs when MACD histogram is negative (bearish momentum)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Skip shorts when MACD histogram is positive (bullish momentum)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    return prediction