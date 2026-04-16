def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low BB width AND low ATR (genuine squeeze)
    true_compression = bb_width < 0.75 and atr_ratio < 0.85
    
    # False compression flags
    stoch_extreme = stoch_k < 20 or stoch_k > 80 or stoch_d < 20 or stoch_d > 80
    far_from_vwap = abs(vwap_deviation) > 0.015
    
    # Skip if compressed but has false signals
    if true_compression and (stoch_extreme or far_from_vwap):
        return "skip"
    
    return prediction