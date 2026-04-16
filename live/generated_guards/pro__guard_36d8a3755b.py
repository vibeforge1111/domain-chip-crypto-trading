def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.1)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # True compression: low volatility + price near middle of bands
    is_compression = atr_ratio < 0.7 and bb_width < 0.1
    
    if is_compression:
        # False compression if price at band extremes
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            return "skip"
        # False compression if VWAP deviation significant
        if abs(vwap_deviation) > 0.006:
            return "skip"
        # False compression if stochastic divergence or extreme
        if stoch_k < 20 or stoch_k > 80 or abs(stoch_k - stoch_d) > 25:
            return "skip"
    
    return prediction