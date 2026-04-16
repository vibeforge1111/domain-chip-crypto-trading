def guard(features: dict, prediction: str) -> str:
    """Filter false breakouts during compression using BB and momentum alignment."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 0.3)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    obv_slope = features.get('obv_slope', 0)
    macd_hist = features.get('macd_histogram', 0)
    
    # True compression: both ATR and BB narrow
    is_compression = atr_ratio < 0.75 and bb_width < 0.18
    
    if is_compression:
        # False compression signals
        stoch_extreme = stoch_k > 78 or stoch_k < 22
        stoch_divergence = abs(stoch_k - stoch_d) > 15
        vwap_displaced = abs(vwap_dev) > 0.008
        momentum_divergent = obv_slope * macd_hist < 0
        
        # Count conflict signals
        conflicts = sum([stoch_extreme, stoch_divergence, vwap_displaced, momentum_divergent])
        
        if conflicts >= 2:
            return "skip"
    
    return prediction