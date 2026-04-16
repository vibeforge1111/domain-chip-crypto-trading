def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum deceleration."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if momentum is flattening (histogram near zero)
    if abs(macd_hist) < 0.0001:
        return "skip"
    
    # Skip longs when histogram is negative (bearish momentum)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Skip shorts when histogram is positive (bullish momentum)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    return prediction