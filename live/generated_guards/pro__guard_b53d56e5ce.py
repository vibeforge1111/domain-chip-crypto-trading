def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compressions using ATR and BB width."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    vwap_dev = features.get('vwap_deviation', 0.0)
    stoch_k = features.get('stoch_k', 50)
    
    # True compression: low BB width AND low ATR ratio
    is_compressed = bb_width < 0.5 and atr_ratio < 0.8
    
    # False compression signals: extreme stochastic OR far from VWAP
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    far_from_vwap = abs(vwap_dev) > 0.015
    
    if is_compressed and (stoch_extreme or far_from_vwap):
        return "skip"
    
    return prediction