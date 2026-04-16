def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # True compression: low ATR ratio AND narrow BBs
    true_compression = atr_ratio < 0.7 and bb_width < 0.3
    
    # False compression: stoch in extreme zones indicates exhaustion not compression
    stoch_extreme = stoch_k > 80 or stoch_k < 20 or stoch_d > 80 or stoch_d < 20
    
    # Price too far from VWAP suggests breakout not compression
    vwap_too_far = abs(vwap_deviation) > 0.02
    
    # Skip if compression setup but indicators suggest false signal
    if true_compression and stoch_extreme:
        return "skip"
    
    # Skip if price extended from VWAP during compression
    if true_compression and vwap_too_far:
        return "skip"
    
    # Skip if 2h RSI in extreme zone during compression
    if true_compression and (rsi_2h < 35 or rsi_2h > 65):
        return "skip"
    
    return prediction