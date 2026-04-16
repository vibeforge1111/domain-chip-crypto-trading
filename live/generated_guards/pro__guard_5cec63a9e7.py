def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration against the direction."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip longs when MACD histogram is negative (bearish momentum deceleration)
    if prediction == "long" and macd_hist < -0.0003:
        return "skip"
    
    # Skip shorts when MACD histogram is positive (bullish momentum deceleration)
    if prediction == "short" and macd_hist > 0.0003:
        return "skip"
    
    return prediction