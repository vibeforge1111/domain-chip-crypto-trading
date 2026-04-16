def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    agree_count = 0
    
    if prediction == "long":
        if stoch_k > stoch_d:
            agree_count += 1
        if vwap_deviation > 0:
            agree_count += 1
        if macd_histogram > 0:
            agree_count += 1
        if obv_slope > 0:
            agree_count += 1
        if bb_pct_b > 0.2:
            agree_count += 1
    else:
        if stoch_k < stoch_d:
            agree_count += 1
        if vwap_deviation < 0:
            agree_count += 1
        if macd_histogram < 0:
            agree_count += 1
        if obv_slope < 0:
            agree_count += 1
        if bb_pct_b < 0.8:
            agree_count += 1
    
    if agree_count < 2:
        return "skip"
    return prediction