def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        signals = 0
        if vwap_dev > 0: signals += 1
        if stoch_k < 70 and stoch_d < 70: signals += 1
        if obv_slope > 0: signals += 1
        if macd_hist > 0: signals += 1
        if bb_pct_b < 0.7 and rsi_2h < 70: signals += 1
        if signals < 2:
            return "skip"
    
    elif prediction == "short":
        signals = 0
        if vwap_dev < 0: signals += 1
        if stoch_k > 30 and stoch_d > 30: signals += 1
        if obv_slope < 0: signals += 1
        if macd_hist < 0: signals += 1
        if bb_pct_b > 0.3 and rsi_2h > 30: signals += 1
        if signals < 2:
            return "skip"
    
    return prediction