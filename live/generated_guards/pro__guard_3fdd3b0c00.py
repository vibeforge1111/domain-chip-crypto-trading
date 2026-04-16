def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    macd_hist = features.get("macd_histogram", 0)
    
    confirm_count = 0
    
    if prediction == "long":
        if obv_slope > 0: confirm_count += 1
        if macd_hist > 0: confirm_count += 1
        if vwap_dev > 0: confirm_count += 1
        if stoch_k > 50: confirm_count += 1
        if rsi_14 > 50 and rsi_14 < 70: confirm_count += 1
        if rsi_2h > 40: confirm_count += 1
    else:
        if obv_slope < 0: confirm_count += 1
        if macd_hist < 0: confirm_count += 1
        if vwap_dev < 0: confirm_count += 1
        if stoch_k < 50: confirm_count += 1
        if rsi_14 < 50 and rsi_14 > 30: confirm_count += 1
        if rsi_2h < 60: confirm_count += 1
    
    return "skip" if confirm_count < 2 else prediction