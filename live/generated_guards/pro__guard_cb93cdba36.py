def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5) * 100
    macd_hist = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    
    confirmations = 0
    
    if prediction == "long":
        if rsi_14 > 50: confirmations += 1
        if rsi_2h > 50: confirmations += 1
        if stoch_k < 80: confirmations += 1
        if macd_hist > 0: confirmations += 1
        if vwap_dev > 0: confirmations += 1
        if obv_slope > 0: confirmations += 1
    elif prediction == "short":
        if rsi_14 < 50: confirmations += 1
        if rsi_2h < 50: confirmations += 1
        if stoch_k > 20: confirmations += 1
        if macd_hist < 0: confirmations += 1
        if vwap_dev < 0: confirmations += 1
        if obv_slope < 0: confirmations += 1
    
    return prediction if confirmations >= 3 else "skip"