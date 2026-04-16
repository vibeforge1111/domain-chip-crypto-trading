def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect compression
    is_compressed = atr_ratio < 0.75 and bb_width < 0.5
    
    if is_compressed:
        # True compression needs momentum alignment
        stoch_aligned = (stoch_k > 60 and stoch_d > 60) or (stoch_k < 40 and stoch_d < 40)
        has_momentum = macd_histogram > 0 or obv_slope > 0
        
        # Skip if compressed but no clear momentum direction
        if prediction == 'long' and not (stoch_aligned and has_momentum):
            return "skip"
        if prediction == 'short' and not (stoch_aligned and (macd_histogram < 0 or obv_slope < 0)):
            return "skip"
    
    return prediction