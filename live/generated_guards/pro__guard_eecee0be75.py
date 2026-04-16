def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if stoch_k < 80 and stoch_d < 80:
            confirmations += 1
        if bb_pct_b < 0.7:
            confirmations += 1
        if vwap_deviation > -0.005:
            confirmations += 1
        if macd_histogram >= 0:
            confirmations += 1
        if rsi_2h < 75:
            confirmations += 1
    elif prediction == "short":
        if stoch_k > 20 and stoch_d > 20:
            confirmations += 1
        if bb_pct_b > 0.3:
            confirmations += 1
        if vwap_deviation < 0.005:
            confirmations += 1
        if macd_histogram <= 0:
            confirmations += 1
        if rsi_2h > 25:
            confirmations += 1
    
    if confirmations < 2:
        return "skip"
    return prediction