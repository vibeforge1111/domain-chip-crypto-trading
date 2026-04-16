def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum deceleration or misaligned indicators."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_14 = features.get("rsi_14", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when momentum is bearish or weakening
    if prediction == "long":
        if macd_hist < -0.0001:
            return "skip"
        if stoch_k > 80 and rsi_14 > 65:
            return "skip"
        if vwap_dev < -0.005:
            return "skip"
        if obv_slope < -0.01:
            return "skip"
    
    # Skip shorts when momentum is bullish or weakening
    if prediction == "short":
        if macd_hist > 0.0001:
            return "skip"
        if stoch_k < 20 and rsi_14 < 35:
            return "skip"
        if vwap_dev > 0.005:
            return "skip"
        if obv_slope > 0.01:
            return "skip"
    
    return prediction