def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and BB width."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    vwap_dev = features.get('vwap_deviation', 0.0)
    
    # True compression: tight BB width + moderate ATR ratio
    is_compressed = bb_width < 0.15 and 0.4 < atr_ratio < 1.2
    
    # False compression: large VWAP deviation (far from value)
    false_compression = abs(vwap_dev) > 0.015
    
    if is_compressed and false_compression:
        return "skip"
    
    return prediction