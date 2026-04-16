def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch = features.get("stoch_k", 50)
    macd = features.get("macd_histogram", 0)
    obv = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    confirmations = 0
    
    if prediction == "long":
        if bb > 0.5: confirmations += 1
        if vwap > 0: confirmations += 1
        if macd > 0: confirmations += 1
        if obv > 0: confirmations += 1
        if stoch < 80 and stoch > 20: confirmations += 1
    elif prediction == "short":
        if bb < 0.5: confirmations += 1
        if vwap < 0: confirmations += 1
        if macd < 0: confirmations += 1
        if obv < 0: confirmations += 1
        if stoch < 80 and stoch > 20: confirmations += 1
    
    return "skip" if confirmations < 2 else prediction