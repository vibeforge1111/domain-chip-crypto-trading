def guard(features: dict, prediction: str) -> str:
    """Skip entries when momentum is decelerating based on MACD histogram."""
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    
    # Detect momentum deceleration: MACD flattening near zero with overbought/oversold
    if prediction == 'long' and 0 < macd < 0.0008 and stoch > 75:
        return "skip"
    if prediction == 'short' and -0.0008 < macd < 0 and stoch < 25:
        return "skip"
    
    return prediction