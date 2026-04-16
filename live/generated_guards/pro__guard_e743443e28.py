def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd_hist = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        bullish_count = 0
        if bb_pct_b > 0.5: bullish_count += 1
        if vwap_dev > 0: bullish_count += 1
        if stoch_k > 20 and stoch_d > 20: bullish_count += 1
        if macd_hist > 0: bullish_count += 1
        if obv_slope > 0 and rsi_2h < 70: bullish_count += 1
        if bullish_count < 2:
            return "skip"
    elif prediction == "short":
        bearish_count = 0
        if bb_pct_b < 0.5: bearish_count += 1
        if vwap_dev < 0: bearish_count += 1
        if stoch_k < 80 and stoch_d < 80: bearish_count += 1
        if macd_hist < 0: bearish_count += 1
        if obv_slope < 0 and rsi_2h > 30: bearish_count += 1
        if bearish_count < 2:
            return "skip"
    
    return prediction