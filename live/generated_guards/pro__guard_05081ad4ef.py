def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    macd_hist = features.get('macd_histogram', 0.0)
    rsi_2h = features.get('rsi_2h', 50.0)
    stoch_k = features.get('stoch_k', 50.0)
    
    # True compression: both BB width and ATR compressed
    is_compression = (bb_width < 0.7) and (atr_ratio < 0.8)
    
    if not is_compression:
        return prediction
    
    # False compression signals lack directional setup
    # Valid compression needs: not centered in BB, aligned momentum
    bb_center_dist = abs(bb_pct_b - 0.5)
    has_direction = bb_center_dist > 0.12
    
    # Momentum must align with prediction direction
    momentum_ok = (prediction == "long" and macd_hist > 0) or \
                  (prediction == "short" and macd_hist < 0)
    
    # Broader context RSI shouldn't be extreme
    context_ok = 35 < rsi_2h < 65
    
    # Stochastic confirms not overextended
    stoch_ok = 20 < stoch_k < 80
    
    if is_compression and has_direction and momentum_ok and context_ok and stoch_ok:
        return prediction
    
    return "skip"