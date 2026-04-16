def guard(features: dict, prediction: str) -> str:
    """Guard against false compression breakouts using ATR and Bollinger Band analysis."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low atr_ratio AND low bb_width
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    if is_compressed:
        # False compression: extreme position within bands during compression
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            return "skip"
        # False compression: far from VWAP during compression
        if abs(vwap_deviation) > 0.007:
            return "skip"
    
    return prediction