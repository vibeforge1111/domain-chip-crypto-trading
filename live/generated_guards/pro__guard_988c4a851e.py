def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compressions - squeeze but with exhausted oscillator or VWAP drift."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True squeeze: both ATR and BB width compressed
    is_squeeze = atr_ratio < 0.7 and bb_width < 0.75
    
    if is_squeeze:
        # False compression: squeeze but stochastic already extended
        if stoch_k > 80 or stoch_k < 20:
            return "skip"
        # False compression: squeeze but price has drifted from VWAP
        if abs(vwap_deviation) > 0.012:
            return "skip"
    
    return prediction