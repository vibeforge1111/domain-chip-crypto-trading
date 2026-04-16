def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # True compression: both bb_width and atr_ratio are low
    is_compression = bb_width < 0.15 and atr_ratio < 0.7
    
    # False signal in compression: extreme stoch zones
    is_extreme = stoch_k < 25 or stoch_k > 75
    
    # False signal in compression: far from fair value
    is_far_from_fair = abs(vwap_dev) > 0.01
    
    if is_compression and (is_extreme or is_far_from_fair):
        return "skip"
    
    return prediction