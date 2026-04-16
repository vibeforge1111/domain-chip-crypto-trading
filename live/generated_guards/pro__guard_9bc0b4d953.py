def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # True compression: low volatility in both ATR and BB
    is_compression = atr_ratio < 0.7 and bb_width < 0.6
    
    if is_compression:
        # False compression flags during compression
        # Price at BB extreme with stretched stochastic
        extreme_bb = bb_pct_b > 0.9 or bb_pct_b < 0.1
        stretched_stoch = (stoch_k > 80 and stoch_d > 80) or (stoch_k < 20 and stoch_d < 20)
        extended_2h = rsi_2h > 75 or rsi_2h < 25
        far_from_vwap = abs(vwap_deviation) > 0.015
        
        false_compression_score = sum([extreme_bb, stretched_stoch, extended_2h, far_from_vwap])
        
        if false_compression_score >= 2:
            return "skip"
    
    return prediction