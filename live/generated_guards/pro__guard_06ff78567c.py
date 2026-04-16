def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression phases to avoid false breakouts."""
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0.0)
    stoch_k = features.get("stoch_k", 50.0)
    
    # Detect true compression: low ATR + narrow BBs
    in_compression = atr_ratio < 0.7 and bb_width < 0.8
    
    if in_compression:
        # False compression filter: avoid extremes where move is exhausted
        bb_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
        vwap_far = abs(vwap_deviation) > 0.015
        stoch_extreme = stoch_k < 20 or stoch_k > 80
        
        if bb_extreme or vwap_far or stoch_extreme:
            return "skip"
    
    return prediction