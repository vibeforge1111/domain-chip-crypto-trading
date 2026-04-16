def guard(features: dict, prediction: str) -> str:
    # True vs false compression detection
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low atr + narrow bands
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    if is_compressed:
        # False compression: extreme stoch divergence or large VWAP drift
        stoch_div = abs(stoch_k - stoch_d) > 15
        if stoch_k < 25 or stoch_k > 75 or stoch_div or abs(vwap_deviation) > 0.008:
            return "skip"
    
    return prediction