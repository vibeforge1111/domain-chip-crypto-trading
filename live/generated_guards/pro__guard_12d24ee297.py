def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    
    # Momentum deceleration check: longs need bullish macd and reasonable stoch
    if prediction == "long":
        if macd < 0 or stoch_k > 88 or obv < 0:
            return "skip"
    
    # Momentum deceleration check: shorts need bearish macd and reasonable stoch
    if prediction == "short":
        if macd > 0 or stoch_k < 12 or obv > 0:
            return "skip"
    
    return prediction