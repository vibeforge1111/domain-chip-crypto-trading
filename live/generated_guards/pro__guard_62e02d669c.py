def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    bullish_signals = 0
    bearish_signals = 0
    
    # VWAP confirmation
    if vwap_dev < -0.001:
        bullish_signals += 1
    elif vwap_dev > 0.001:
        bearish_signals += 1
    
    # Stochastic confirmation
    if stoch_k < 30:
        bullish_signals += 1
    elif stoch_k > 70:
        bearish_signals += 1
    
    # OBV slope confirmation
    if obv_slope > 0:
        bullish_signals += 1
    elif obv_slope < 0:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if macd_hist > 0:
        bullish_signals += 1
    elif macd_hist < 0:
        bearish_signals += 1
    
    # Bollinger Bands position confirmation
    if bb_pct_b < 0.25:
        bullish_signals += 1
    elif bb_pct_b > 0.75:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals >= 2:
        return prediction
    elif prediction == "short" and bearish_signals >= 2:
        return prediction
    
    return "skip"