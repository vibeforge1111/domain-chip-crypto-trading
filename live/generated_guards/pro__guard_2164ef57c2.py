def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using ATR ratio, BB width, and VWAP deviation."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: both volatility measures low
    is_compression = bb_width < 0.12 and atr_ratio < 0.75
    
    # False compression: stoch at extreme or far from VWAP
    is_valid_compression = 20 < stoch_k < 80 and abs(vwap_deviation) < 0.015
    
    if is_compression and not is_valid_compression:
        return "skip"
    return prediction