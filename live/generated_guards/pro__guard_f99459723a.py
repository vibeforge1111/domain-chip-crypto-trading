def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
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
    
    # Stochastic confirmation
    if stoch_k > 50:
        bullish_signals += 1
    elif stoch_k < 50:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if macd_histogram > 0:
        bullish_signals += 1
    elif macd_histogram < 0:
        bearish_signals += 1
    
    # OBV slope confirmation
    if obv_slope > 0:
        bullish_signals += 1
    elif obv_slope < 0:
        bearish_signals += 1
    
    # VWAP deviation confirmation
    if vwap_deviation > 0:
        bullish_signals += 1
    elif vwap_deviation < 0:
        bearish_signals += 1
    
    # Bollinger Band position confirmation
    if bb_pct_b > 0.5:
        bullish_signals += 1
    elif bb_pct_b < 0.5:
        bearish_signals += 1
    
    # Wider timeframe RSI confirmation
    if rsi_2h > 55:
        bullish_signals += 1
    elif rsi_2h < 45:
        bearish_signals += 1
    
    # Require at least 2 signals to agree with prediction
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction