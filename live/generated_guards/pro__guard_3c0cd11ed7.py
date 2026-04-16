def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # True compression: low ATR + narrow BBs
    is_compressed = atr_ratio < 0.7 and bb_width < 0.35
    
    # False compression: stoch at extremes despite compression
    stoch_extreme = stoch_k < 20 or stoch_k > 80 or stoch_d < 20 or stoch_d > 80
    
    if is_compressed and stoch_extreme:
        return "skip"
    
    return prediction