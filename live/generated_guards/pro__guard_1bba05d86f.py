def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using bb_width, atr_ratio, and oscillators."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # True compression: low bb_width AND low atr_ratio
    is_compressed = bb_width < 0.15 and atr_ratio < 0.8
    
    if is_compressed:
        # False compression: stochastic divergence (k and d disagree)
        if abs(stoch_k - stoch_d) > 20:
            return "skip"
        # False compression: large VWAP deviation despite compression
        if abs(vwap_dev) > 0.02:
            return "skip"
    
    return prediction