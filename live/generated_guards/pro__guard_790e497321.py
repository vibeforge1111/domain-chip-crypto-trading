def guard(features: dict, prediction: str) -> str:
    """Reject trades during false compressions (compressed but extreme BB position)."""
    bb_width = features['bb_width']
    atr_ratio = features['atr_ratio']
    bb_pct_b = features['bb_pct_b']
    vwap_deviation = features['vwap_deviation']
    
    # True compression: both BB width and ATR compressed
    is_compressed = bb_width < 0.15 and atr_ratio < 0.8
    
    # False compression: compressed but price at extreme BB position
    is_extreme_bb = bb_pct_b < 0.12 or bb_pct_b > 0.88
    
    if is_compressed and is_extreme_bb:
        return "skip"
    
    # True compression needs proximity to VWAP for validity
    if is_compressed and abs(vwap_deviation) > 0.018:
        return "skip"
    
    return prediction