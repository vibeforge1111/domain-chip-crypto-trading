def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard - requires 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation: valid zone (30-70) for either direction
    rsi = features.get("rsi_14", 50)
    if 30 < rsi < 70:
        confirmations += 1
    
    # Stochastic confirmation: not in extreme zone
    stoch_k = features.get("stoch_k", 50)
    if 20 < stoch_k < 80:
        confirmations += 1
    
    # VWAP alignment: price near VWAP (within 0.5%)
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.005:
        confirmations += 1
    
    # OBV momentum: slope matches direction
    obv_slope = features.get("obv_slope", 0)
    if (prediction == "long" and obv_slope > 0) or (prediction == "short" and obv_slope < 0):
        confirmations += 1
    
    # MACD histogram confirmation
    macd = features.get("macd_histogram", 0)
    if (prediction == "long" and macd > 0) or (prediction == "short" and macd < 0):
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations >= 2:
        return prediction
    return "skip"