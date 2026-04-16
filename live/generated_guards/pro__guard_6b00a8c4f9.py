def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    confirmations = 0
    
    if prediction == "long":
        if vwap_deviation > 0: confirmations += 1
        if stoch_k < 80 and stoch_d < 80: confirmations += 1
        if obv_slope > 0: confirmations += 1
        if macd_histogram > 0: confirmations += 1
        if rsi_2h < 70 and bb_pct_b < 0.9: confirmations += 1
    else:
        if vwap_deviation < 0: confirmations += 1
        if stoch_k > 20 and stoch_d > 20: confirmations += 1
        if obv_slope < 0: confirmations += 1
        if macd_histogram < 0: confirmations += 1
        if rsi_2h > 30 and bb_pct_b > 0.1: confirmations += 1
    
    return "skip" if confirmations < 2 else prediction