def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    rsi_14 = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    macd_hist = features.get("macd_histogram", 0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_2h = features.get("rsi_2h", 50)
    
    agree_count = 0
    
    if prediction == "long":
        if rsi_14 < 70: agree_count += 1
        if stoch_k < 80: agree_count += 1
        if vwap_dev > 0: agree_count += 1
        if macd_hist > 0: agree_count += 1
        if bb_pct_b < 0.6: agree_count += 1
        if rsi_2h < 70: agree_count += 1
    else:
        if rsi_14 > 30: agree_count += 1
        if stoch_k > 20: agree_count += 1
        if vwap_dev < 0: agree_count += 1
        if macd_hist < 0: agree_count += 1
        if bb_pct_b > 0.4: agree_count += 1
        if rsi_2h > 30: agree_count += 1
    
    return "skip" if agree_count < 2 else prediction