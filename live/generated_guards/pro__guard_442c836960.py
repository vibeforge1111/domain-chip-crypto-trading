def guard(features: dict, prediction: str) -> str:
    """Filter trades with false compression (low vol + weak momentum)."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression: low BB width AND low ATR ratio
    is_compressed = bb_width < 0.15 and atr_ratio < 0.7
    
    if is_compressed:
        # False compression signals: extreme stochastics OR weak momentum confirmation
        stoch_extreme = stoch_k > 80 or stoch_k < 20 or stoch_d > 80 or stoch_d < 20
        weak_momentum = abs(macd_histogram) < 0.0005 and obv_slope < 0
        
        if stoch_extreme or weak_momentum:
            return "skip"
    
    return prediction