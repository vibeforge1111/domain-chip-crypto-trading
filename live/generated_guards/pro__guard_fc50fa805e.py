def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if prediction == "long":
        if stoch_k < 35:
            confirmations += 1
        if vwap_dev < -0.001:
            confirmations += 1
        if obv_slope > 0:
            confirmations += 1
        if macd_hist > 0:
            confirmations += 1
        if rsi_2h < 60:
            confirmations += 1
        if bb_pct_b < 0.3:
            confirmations += 1
    
    elif prediction == "short":
        if stoch_k > 65:
            confirmations += 1
        if vwap_dev > 0.001:
            confirmations += 1
        if obv_slope < 0:
            confirmations += 1
        if macd_hist < 0:
            confirmations += 1
        if rsi_2h > 40:
            confirmations += 1
        if bb_pct_b > 0.7:
            confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"