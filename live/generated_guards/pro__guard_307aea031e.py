def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using bb_width, atr_ratio, and oscillators."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    stoch_k = features.get('stoch_k', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    macd_hist = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: narrowing bands + low volatility
    is_compression = bb_width < 0.75 and atr_ratio < 0.85
    
    if is_compression and prediction != "skip":
        # False compression flags
        stoch_extreme = stoch_k > 85 or stoch_k < 15
        vwap_far = abs(vwap_dev) > 0.015
        weak_momentum = abs(macd_hist) < 0.0003
        rsi_divergent = rsi_2h > 70 or rsi_2h < 30
        
        # Reject if multiple false signals present
        false_flags = sum([stoch_extreme, vwap_far, weak_momentum, rsi_divergent])
        if false_flags >= 2:
            return "skip"
    
    return prediction