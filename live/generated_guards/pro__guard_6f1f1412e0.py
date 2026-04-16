def guard(features: dict, prediction: str) -> str:
    """Filter trades by detecting true vs false compression using ATR and Bollinger width."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    
    # True compression: both compressed simultaneously (reliable)
    # False compression: only one compressed (unreliable setup)
    both_compressed = atr_ratio < 0.85 and bb_width < 0.18
    one_compressed = (atr_ratio < 0.85) != (bb_width < 0.18)
    
    if one_compressed:
        return "skip"
    
    if both_compressed:
        # In true compression, require momentum confirmation
        if features.get("momentum_score", 0) < 0.25:
            return "skip"
        # Avoid overbought/oversold extremes in compression setups
        if features.get("stoch_k", 50) > 85 or features.get("stoch_k", 50) < 15:
            return "skip"
    
    return prediction