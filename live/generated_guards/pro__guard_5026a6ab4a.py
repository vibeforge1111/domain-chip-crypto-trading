def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, stoch, and bb_pct_b."""
    in_compression = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 0.5) < 0.25
    
    if in_compression and prediction != "skip":
        # False breakout: stoch at extreme during compression
        if features.get('stoch_k', 50) > 80 or features.get('stoch_k', 50) < 20:
            return "skip"
        
        # False signal: bb_pct_b at band extremes
        bb_pos = features.get('bb_pct_b', 0.5)
        if bb_pos < 0.08 or bb_pos > 0.92:
            return "skip"
    
    return prediction