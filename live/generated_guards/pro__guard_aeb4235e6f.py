def guard(features: dict, prediction: str) -> str:
    """Guard against trades when macd_histogram shows momentum against entry direction."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip longs when macd_histogram is negative (bearish momentum deceleration)
    if prediction == "long" and macd_hist < -0.0001:
        return "skip"
    
    # Skip shorts when macd_histogram is positive (bullish momentum deceleration)
    if prediction == "short" and macd_hist > 0.0001:
        return "skip"
    
    return prediction