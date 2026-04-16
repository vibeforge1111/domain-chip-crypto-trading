def guard(features: dict, prediction: str) -> str:
    """Guard function using macd_histogram for momentum deceleration filtering."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs if momentum decelerating and overbought
    if prediction == "long" and macd_hist < -0.0001 and stoch_k > 70:
        return "skip"
    
    # Skip shorts if momentum decelerating upward and oversold
    if prediction == "short" and macd_hist < -0.0001 and stoch_k < 30:
        return "skip"
    
    return prediction