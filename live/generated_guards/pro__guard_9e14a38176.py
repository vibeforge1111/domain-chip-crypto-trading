def guard(features: dict, prediction: str) -> str:
    # True vs false compression detection using atr_ratio + bb_width with new momentum features
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Compression pattern: high ATR but narrow BB (squeeze)
    is_compression = atr_ratio > 1.2 and bb_width < 0.15
    
    # False compression: extended oscillators conflicting with higher timeframe
    stoch_extreme = stoch_k > 85 or stoch_k < 15
    rsi_2h_extreme = rsi_2h > 70 or rsi_2h < 30
    
    # Also check for divergence from fair value
    far_from_vwap = abs(vwap_dev) > 0.015
    
    # Skip if compression with extended conditions suggesting false breakout
    if is_compression and stoch_extreme and rsi_2h_extreme and far_from_vwap:
        return "skip"
    
    return prediction