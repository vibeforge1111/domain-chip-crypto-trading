def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    
    bullish = 0
    bearish = 0
    
    if vwap > 0: bullish += 1
    elif vwap < 0: bearish += 1
    
    if stoch_k < 80: bullish += 1
    else: bearish += 1
    
    if obv > 0: bullish += 1
    elif obv < 0: bearish += 1
    
    if macd > 0: bullish += 1
    elif macd < 0: bearish += 1
    
    if bb < 0.8: bullish += 1
    else: bearish += 1
    
    if prediction == "long" and bullish >= 2:
        return prediction
    elif prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"