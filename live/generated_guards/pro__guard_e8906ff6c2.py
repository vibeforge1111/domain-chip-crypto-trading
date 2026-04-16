def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # True compression requires BOTH low atr AND low bb_width
    true_compression = atr_ratio < 0.7 and bb_width < 0.35
    
    # Momentum needs stoch + volume + macd confirmation
    has_momentum = (stoch_k > 25 or stoch_d > 25) and abs(obv_slope) > 0 and abs(macd_histogram) > 0
    
    # Skip if compressed but no momentum building (false compression)
    if true_compression and not has_momentum:
        return "skip"
    
    return prediction