def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # True compression: narrow BB AND low ATR AND price near middle of bands
    is_compressed = bb_width < 0.5 and atr_ratio < 0.8
    
    # False compression: compressed but price at extremes (pre-breakout trap)
    is_false_compression = is_compressed and (bb_pct_b < 0.15 or bb_pct_b > 0.85)
    
    if is_false_compression:
        return "skip"
    
    return prediction