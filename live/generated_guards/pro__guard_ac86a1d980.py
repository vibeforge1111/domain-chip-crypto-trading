def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression: both ATR and BB width must be low
    is_compressed = atr_ratio < 0.7 and bb_width < 0.15
    
    if is_compressed:
        # Momentum must be building for valid breakout
        momentum_confirming = (stoch_k > 60 or stoch_k < 40 or
                               abs(macd_histogram) > 0.0005 or
                               abs(obv_slope) > 0.1)
        if not momentum_confirming:
            return "skip"
    
    return prediction