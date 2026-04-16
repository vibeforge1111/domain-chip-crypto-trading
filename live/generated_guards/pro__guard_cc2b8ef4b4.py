def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # High confidence entry zones: BB extremes
    at_lower_extreme = bb_pct_b < 0.05
    at_upper_extreme = bb_pct_b > 0.95
    
    if not at_lower_extreme and not at_upper_extreme:
        return "skip"
    
    # Long at lower BB extreme: confirm with RSI and VWAP
    if prediction == "long" and at_lower_extreme:
        if rsi_2h < 40 and vwap_deviation < 0:
            return prediction
        return "skip"
    
    # Short at upper BB extreme: confirm with RSI and VWAP
    if prediction == "short" and at_upper_extreme:
        if rsi_2h > 60 and vwap_deviation > 0:
            return prediction
        return "skip"
    
    return "skip"