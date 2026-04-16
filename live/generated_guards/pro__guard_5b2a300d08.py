def guard(features: dict, prediction: str) -> str:
    # True compression detected when bb_width is low
    if features.get('bb_width', 1) > 0.18:
        return prediction
    
    # False compression: in tight bands but at extreme BB position (likely breakout)
    bb_pos = features.get('bb_pct_b', 0.5)
    if bb_pos < 0.12 or bb_pos > 0.88:
        return "skip"
    
    # False compression: strong directional momentum in compression
    if abs(features.get('macd_histogram', 0)) > 0.004:
        return "skip"
    
    # False compression: stoch at extremes during compression (exhaustion)
    stoch = features.get('stoch_k', 50)
    if stoch < 15 or stoch > 85:
        return "skip"
    
    # ATR check: avoid when volatility is abnormally compressed
    if features.get('atr_ratio', 1.0) < 0.6:
        return "skip"
    
    return prediction