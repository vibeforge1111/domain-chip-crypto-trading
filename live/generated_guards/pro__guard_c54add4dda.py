def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using atr_ratio, bb_width, and bb_pct_b."""
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: low bb_width, moderate atr_ratio
    is_compressed = bb_width < 0.25 and atr_ratio < 0.7
    
    # False compression: compressed but at Bollinger extremes
    is_false_compression = is_compressed and (bb_pct_b < 0.15 or bb_pct_b > 0.85)
    
    # Stochastic confirms valid entry zone (not overbought/oversold)
    stoch_valid = 25 < stoch_k < 75
    
    if is_false_compression and not stoch_valid:
        return "skip"
    
    return prediction