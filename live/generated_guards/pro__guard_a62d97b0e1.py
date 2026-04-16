def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using BB width, ATR ratio, and positioning."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # True compression: tight BB + low ATR volatility
    is_compressed = bb_width < 0.15 and atr_ratio < 0.7
    
    if is_compressed:
        # False compression: price at band extremes (distribution, not consolidation)
        if bb_pct_b > 0.88 or bb_pct_b < 0.12:
            return "skip"
        # False compression: stochastic extreme (momentum exhausted in compression)
        if stoch_k > 78 or stoch_k < 22:
            return "skip"
    
    return prediction