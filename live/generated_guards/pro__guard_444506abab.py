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
    
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic momentum
    if stoch_k > 30:
        bullish_count += 1
    if stoch_k < 70:
        bearish_count += 1
    
    # VWAP deviation
    if vwap_dev > -0.015:
        bullish_count += 1
    if vwap_dev < 0.015:
        bearish_count += 1
    
    # OBV slope
    if obv_slope > 0:
        bullish_count += 1
    if obv_slope < 0:
        bearish_count += 1
    
    # MACD histogram
    if macd_hist > 0:
        bullish_count += 1
    if macd_hist < 0:
        bearish_count += 1
    
    # RSI 2h context
    if rsi_2h < 60:
        bullish_count += 1
    if rsi_2h > 40:
        bearish_count += 1
    
    if prediction == "long" and bearish_count >= 3:
        return "skip"
    if prediction == "short" and bullish_count >= 3:
        return "skip"
    
    return prediction