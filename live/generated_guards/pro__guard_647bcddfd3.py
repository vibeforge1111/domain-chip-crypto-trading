def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0.0)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: both ATR and BB width are low simultaneously
    is_true_compression = atr_ratio < 0.7 and bb_width < 0.15
    
    # Skip if price is far from VWAP (weak signal quality)
    if abs(vwap_deviation) > 0.015:
        return "skip"
    
    # In compression, avoid extremes (likely reversal setup, not continuation)
    if is_true_compression and (stoch_k > 75 or stoch_k < 25):
        return "skip"
    
    # In compression, avoid band extremes (false breakouts common here)
    if is_true_compression and (bb_pct_b > 0.92 or bb_pct_b < 0.08):
        return "skip"
    
    return prediction