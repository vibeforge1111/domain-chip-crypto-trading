def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and BB width."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # True compression: low ATR and narrow BBs
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    # Price too far from VWAP during compression = likely false signal
    if is_compressed and abs(vwap_dev) > 0.008:
        return "skip"
    
    # Weak stochastic momentum during compression = false breakout risk
    stoch_weak = 30 < stoch_k < 70 and 30 < stoch_d < 70
    if is_compressed and stoch_weak:
        return "skip"
    
    return prediction