def guard(features: dict, prediction: str) -> str:
    """Detect false compression: tight range at market extremes often fails."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # True compression: both ATR and BB are low
    is_compression = (atr_ratio < 0.7 and bb_width < 0.015)
    
    # False compression: compression at extremes (price far from bands)
    at_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
    
    if is_compression and at_extreme:
        return "skip"
    
    return prediction