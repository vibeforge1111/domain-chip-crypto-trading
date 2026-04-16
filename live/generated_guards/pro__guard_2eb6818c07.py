def guard(features: dict, prediction: str) -> str:
    """Filter false breakouts from compression using ATR, BB width, and oscillators."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: both ATR and BB width low
    is_compression = atr_ratio < 0.6 and bb_width < 0.12
    
    # Warning signs for false breakout
    stoch_divergence = abs(stoch_k - stoch_d) > 15
    stretched_from_vwap = abs(vwap_deviation) > 0.004
    
    if is_compression and (stoch_divergence or stretched_from_vwap):
        return "skip"
    
    return prediction