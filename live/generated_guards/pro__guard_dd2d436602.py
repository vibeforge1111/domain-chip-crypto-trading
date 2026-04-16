def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and BB width."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    
    # Detect compression: both ATR and BB width must be low
    if atr_ratio > 0.75 or bb_width > 0.75:
        return prediction
    
    # False compression filter: stoch extreme during compression
    stoch_k = features.get('stoch_k', 50)
    if stoch_k < 20 or stoch_k > 80:
        return 'skip'
    
    # False compression: price too far from VWAP during "compression"
    if abs(features.get('vwap_deviation', 0)) > 0.02:
        return 'skip'
    
    # False compression: weak OBV slope (no accumulation/distribution)
    if features.get('obv_slope', 0) <= 0:
        return 'skip'
    
    return prediction