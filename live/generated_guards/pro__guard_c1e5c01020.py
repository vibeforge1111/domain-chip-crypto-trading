def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    confirmations = 0
    
    if prediction == "long":
        if rsi < 70 and rsi_2h < 70:
            confirmations += 1
        if stoch_k < 80:
            confirmations += 1
        if bb < 0.85:
            confirmations += 1
        if vwap < 0.005 or obv > 0:
            confirmations += 1
        if macd >= -0.0001:
            confirmations += 1
    else:
        if rsi > 30 and rsi_2h > 30:
            confirmations += 1
        if stoch_k > 20:
            confirmations += 1
        if bb > 0.15:
            confirmations += 1
        if vwap > -0.005 or obv < 0:
            confirmations += 1
        if macd <= 0.0001:
            confirmations += 1
    
    if confirmations < 2:
        return "skip"
    
    return prediction