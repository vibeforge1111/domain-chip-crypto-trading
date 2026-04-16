def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using ATR, BB width, and BB position."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # True compression: low atr_ratio AND low bb_width
    is_compressed = atr_ratio < 0.7 and bb_width < 0.8
    
    # If compressed, price should be near middle of bands for valid breakout
    if is_compressed and (bb_pct_b < 0.15 or bb_pct_b > 0.85):
        return "skip"
    
    return prediction