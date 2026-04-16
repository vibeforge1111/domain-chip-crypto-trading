def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    bullish_signals = 0
    bearish_signals = 0
    
    # Momentum confirmation
    if rsi_2h < 65:
        bullish_signals += 1
    elif rsi_2h > 35:
        bearish_signals += 1
    
    # VWAP confirmation
    if vwap_dev < 0.005:
        bullish_signals += 1
    elif vwap_dev > 0.005:
        bearish_signals += 1
    
    # Stochastic confirmation
    if stoch_k < 75 and stoch_d < 75:
        bullish_signals += 1
    elif stoch_k > 25 and stoch_d > 25:
        bearish_signals += 1
    
    # MACD confirmation
    if macd_hist > 0:
        bullish_signals += 1
    elif macd_hist < 0:
        bearish_signals += 1
    
    # OBV confirmation
    if obv_slope > 0:
        bullish_signals += 1
    elif obv_slope < 0:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals >= 2:
        return prediction
    elif prediction == "short" and bearish_signals >= 2:
        return prediction
    
    return "skip"