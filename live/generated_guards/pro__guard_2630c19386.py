def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to filter bad signals."""
    bb_width = features.get('bb_width', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low bb_width AND low atr_ratio
    is_compressed = bb_width < 0.3 and atr_ratio < 0.8
    
    # False compression: compressed but overextended (stoch stretched + away from VWAP)
    if is_compressed and stoch_k > 75 and abs(vwap_deviation) > 0.01:
        return "skip"
    
    return prediction