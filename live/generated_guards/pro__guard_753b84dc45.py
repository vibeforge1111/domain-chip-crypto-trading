def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Detect compression: low ATR and narrow BB
    is_compression = atr_ratio < 0.7 and bb_width < 0.4
    
    if is_compression and prediction != "skip":
        # True compression should show momentum building: strong volume + oversold
        momentum_ready = obv_slope > 0.001 and stoch_k < 25
        if not momentum_ready:
            return "skip"
    
    return prediction