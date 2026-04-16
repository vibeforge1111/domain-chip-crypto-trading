def guard(features: dict, prediction: str) -> str:
    # Detect false compression: BB squeeze without volatility confirmation
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # False compression: tight BB but no volatility expansion
    if bb_width < 0.35 and atr_ratio < 0.75:
        return "skip"
    
    # Weak momentum without trend confirmation
    if features.get('momentum_score', 0.5) < 0.35 and abs(vwap_dev) < 0.005:
        return "skip"
    
    return prediction