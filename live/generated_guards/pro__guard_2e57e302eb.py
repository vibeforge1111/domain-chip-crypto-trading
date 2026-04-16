def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when momentum decelerating (neg macd hist + neg obv slope)
    if prediction == "long" and macd_hist < -0.0003 and obv_slope < 0:
        return "skip"
    
    # Skip shorts when momentum decelerating (pos macd hist + overbought stoch)
    if prediction == "short" and macd_hist > 0.0003 and stoch_k > 75:
        return "skip"
    
    return prediction