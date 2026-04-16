def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        confirmations = 0
        if bb_pct_b < 0.35: confirmations += 1  # Near lower band
        if vwap_dev > 0: confirmations += 1  # Above VWAP
        if stoch_k < 70 and stoch_d < 70: confirmations += 1  # Not overbought
        if obv_slope > 0: confirmations += 1  # Bullish volume
        if macd_hist > 0: confirmations += 1  # Positive MACD
        if confirmations < 2: return "skip"
    
    elif prediction == "short":
        confirmations = 0
        if bb_pct_b > 0.65: confirmations += 1  # Near upper band
        if vwap_dev < 0: confirmations += 1  # Below VWAP
        if stoch_k > 30 and stoch_d > 30: confirmations += 1  # Not oversold
        if obv_slope < 0: confirmations += 1  # Bearish volume
        if macd_hist < 0: confirmations += 1  # Negative MACD
        if confirmations < 2: return "skip"
    
    return prediction