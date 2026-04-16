def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    rsi = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pos = features.get("bb_pct_b", 0.5)
    macd_hist = features.get("macd_histogram", 0)
    obv = features.get("obv_slope", 0)
    
    if prediction == "long":
        if 30 <= rsi <= 70: confirmations += 1
        if stoch_k < 80: confirmations += 1
        if vwap_dev > 0: confirmations += 1
        if 0.1 <= bb_pos <= 0.85: confirmations += 1
        if macd_hist >= 0: confirmations += 1
    else:
        if 30 <= rsi <= 70: confirmations += 1
        if stoch_k > 20: confirmations += 1
        if vwap_dev < 0: confirmations += 1
        if 0.15 <= bb_pos <= 0.9: confirmations += 1
        if macd_hist <= 0: confirmations += 1
    
    return "skip" if confirmations < 2 else prediction