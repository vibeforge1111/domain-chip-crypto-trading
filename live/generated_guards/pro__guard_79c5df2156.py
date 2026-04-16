def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and stochastics."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    
    # True compression: low ATR and tight BB bands
    in_compression = atr_ratio < 0.65 and bb_width < 0.3
    
    if in_compression:
        stoch_k = features.get('stoch_k', 50)
        stoch_d = features.get('stoch_d', 50)
        
        # False compression: stochastics at extremes (exhaustion), reject
        if (stoch_k > 75 and stoch_d > 75) or (stoch_k < 25 and stoch_d < 25):
            return "skip"
    
    return prediction