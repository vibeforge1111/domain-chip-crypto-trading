def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using ATR+BB width combination."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    
    # Detecting false compression: low ATR but wide BBs
    if atr_ratio < 0.75:
        if bb_width > 1.15:
            return "skip"
    
    # Skip if price at extreme BB position
    bb_pct_b = features.get('bb_pct_b', 0.5)
    if bb_pct_b > 0.92 or bb_pct_b < 0.08:
        return "skip"
    
    # Skip if too far from VWAP (indicating poor entry)
    if abs(features.get('vwap_deviation', 0)) > 0.015:
        return "skip"
    
    return prediction