def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, BB width, and momentum."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low ATR + low BB width
    is_compressed = atr_ratio < 0.7 and bb_width < 0.35
    
    if is_compressed:
        # False compression: weak momentum and neutral stochastics
        no_momentum = abs(obv_slope) < 0.02 and abs(macd_histogram) < 0.002
        neutral_stoch = 35 < stoch_k < 65 and 35 < stoch_d < 65
        
        if no_momentum and neutral_stoch:
            return "skip"
    
    # Skip extended prices in compression (likely false setup)
    if is_compressed and abs(vwap_deviation) > 0.015:
        return "skip"
    
    return prediction