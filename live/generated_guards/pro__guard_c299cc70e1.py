def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    agree = 0
    
    if prediction == "long":
        if vwap_dev > 0: agree += 1
        if stoch_k > 30 and stoch_d > 30: agree += 1
        if obv > 0: agree += 1
        if macd > 0: agree += 1
        if rsi_2h > 50: agree += 1
    else:
        if vwap_dev < 0: agree += 1
        if stoch_k < 70 and stoch_d < 70: agree += 1
        if obv < 0: agree += 1
        if macd < 0: agree += 1
        if rsi_2h < 50: agree += 1
    
    if agree < 2:
        return "skip"
    return prediction