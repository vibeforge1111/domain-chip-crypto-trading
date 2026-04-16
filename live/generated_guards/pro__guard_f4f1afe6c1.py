def guard(features: dict, prediction: str) -> str:
    """Detect false compression: low volatility but no directional setup."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0.0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression detected: both ATR and BB are tight
    is_compression = atr_ratio < 0.7 and bb_width < 0.015
    
    if is_compression:
        # False compression: oscillators in no-man's land, VWAP centered
        no_direction = (35 < stoch_k < 65 and 35 < stoch_d < 65)
        vwap_centered = abs(vwap_deviation) < 0.003
        rsi_neutral = 40 < rsi_2h < 60
        
        if no_direction and vwap_centered and rsi_neutral:
            return "skip"
    
    return prediction