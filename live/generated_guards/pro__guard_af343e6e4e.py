def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, Bollinger width, and positioning."""
    bb_width = features.get('bb_width', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    
    # False compression: tight BB but high ATR (expansion imminent)
    false_compression = bb_width < 0.2 and atr_ratio > 1.2
    
    # Compressed but extreme stoch (reversal likely)
    extreme_stoch_compression = bb_width < 0.25 and (stoch_k > 80 or stoch_k < 20)
    
    # Compressed but far from VWAP (unstable)
    unstable_compression = bb_width < 0.2 and vwap_dev > 0.008
    
    if false_compression or extreme_stoch_compression or unstable_compression:
        return "skip"
    return prediction