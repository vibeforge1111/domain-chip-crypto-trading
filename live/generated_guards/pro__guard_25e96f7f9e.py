def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using bb_width and atr_ratio."""
    bb_width = features.get('bb_width', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # True compression: low bb_width + low atr_ratio
    true_compression = bb_width < 0.5 and atr_ratio < 0.8
    
    # False compression: stretched from VWAP + near band edge + stoch extreme
    stretched = abs(vwap_deviation) > 0.005
    band_edge = bb_pct_b > 0.85 or bb_pct_b < 0.15
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    false_squeeze = stretched and band_edge and stoch_extreme
    
    if true_compression and false_squeeze:
        return "skip"
    
    return prediction