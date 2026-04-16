def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using bb_width and atr_ratio."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # False compression: tight bands but elevated volatility (volatile consolidation)
    if bb_width < 0.5 and atr_ratio > 1.2:
        return "skip"
    
    # False compression: compressed but at band extremes (pending squeeze release)
    if bb_width < 0.4 and (bb_pct_b < 0.15 or bb_pct_b > 0.85):
        return "skip"
    
    return prediction