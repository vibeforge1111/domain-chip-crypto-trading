def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    bullish_count = 0
    bearish_count = 0
    
    if vwap_dev > 0.001:
        bullish_count += 1
    elif vwap_dev < -0.001:
        bearish_count += 1
    
    if bb_pct > 0.6:
        bullish_count += 1
    elif bb_pct < 0.4:
        bearish_count += 1
    
    if obv_slope > 0:
        bullish_count += 1
    elif obv_slope < 0:
        bearish_count += 1
    
    if macd_hist > 0:
        bullish_count += 1
    elif macd_hist < 0:
        bearish_count += 1
    
    if rsi_2h > 55:
        bullish_count += 1
    elif rsi_2h < 45:
        bearish_count += 1
    
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction