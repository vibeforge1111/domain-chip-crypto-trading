def guard(features: dict, prediction: str) -> str:
    """Reject false compressions: low bb_width but high atr_ratio (volatile squeeze)."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # True compression: low bb_width, moderate volatility
    # False compression: compressed but ATR expanding (about to move violently)
    if bb_width < 0.85 and atr_ratio > 1.25:
        return "skip"
    
    # Also reject if compressed but price at extreme BB position
    if bb_width < 0.8 and (bb_pct_b < 0.2 or bb_pct_b > 0.8):
        return "skip"
    
    return prediction