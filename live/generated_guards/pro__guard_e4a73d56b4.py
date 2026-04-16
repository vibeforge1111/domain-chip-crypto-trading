def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    bullish_signals = 0
    bearish_signals = 0
    
    if bb_pct_b < 0.25:
        bullish_signals += 1
    elif bb_pct_b > 0.75:
        bearish_signals += 1
    
    if vwap_deviation < 0:
        bullish_signals += 1
    elif vwap_deviation > 0:
        bearish_signals += 1
    
    if stoch_k < 25 and stoch_d < 25:
        bullish_signals += 1
    elif stoch_k > 75 and stoch_d > 75:
        bearish_signals += 1
    
    if obv_slope > 0:
        bullish_signals += 1
    elif obv_slope < 0:
        bearish_signals += 1
    
    if macd_histogram > 0:
        bullish_signals += 1
    elif macd_histogram < 0:
        bearish_signals += 1
    
    if rsi_2h < 40:
        bullish_signals += 1
    elif rsi_2h > 60:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals >= 2:
        return prediction
    elif prediction == "short" and bearish_signals >= 2:
        return prediction
    
    return "skip"