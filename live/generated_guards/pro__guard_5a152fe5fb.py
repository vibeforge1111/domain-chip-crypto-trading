def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and BB width."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # True compression: low ATR + tight BB
    is_compressed = atr_ratio < 0.85 and bb_width < 0.18
    
    # False compression: price at extreme BB position during compression
    is_extreme = bb_pct_b < 0.25 or bb_pct_b > 0.75
    
    # Skip if compressed but at BB extremes (false compression)
    if is_compressed and is_extreme:
        return "skip"
    
    return prediction