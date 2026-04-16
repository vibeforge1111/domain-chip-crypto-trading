def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating (macd_histogram fading)."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    
    # Longs: reject if MACD negative or momentum fading (price up, MACD down)
    if prediction == "long":
        if macd < 0:
            return "skip"
        if stoch > 75 and obv < 0:
            return "skip"
    
    # Shorts: reject if MACD positive or momentum fading
    if prediction == "short":
        if macd > 0:
            return "skip"
        if stoch < 25 and obv > 0:
            return "skip"
    
    return prediction