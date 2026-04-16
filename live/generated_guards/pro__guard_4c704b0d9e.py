def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.2)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    is_compressed = atr_ratio < 0.75 and bb_width < 0.18
    
    if is_compressed:
        if bb_pct_b > 0.88 or bb_pct_b < 0.12:
            return "skip"
        if min(stoch_k, stoch_d) < 20 or max(stoch_k, stoch_d) > 80:
            return "skip"
        if obv_slope < 0 and prediction == "long":
            return "skip"
        if obv_slope > 0 and prediction == "short":
            return "skip"
        if rsi_2h > 70 or rsi_2h < 30:
            return "skip"
    
    return prediction