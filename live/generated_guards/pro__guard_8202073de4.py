def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 0)
    atr_ratio = features.get('atr_ratio', 1)
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # True compression: BB narrowing AND ATR contracting
    if bb_width > 0.25 or atr_ratio > 0.9:
        return prediction  # No compression, let signal pass normally
    
    # Compression detected - filter false breakouts
    # False compression: extreme RSI or price far from VWAP
    if rsi_14 < 25 or rsi_14 > 75:
        return "skip"
    if rsi_2h < 30 or rsi_2h > 70:
        return "skip"
    if abs(vwap_deviation) > 0.015:
        return "skip"
    if stoch_k < 15 or stoch_k > 85:
        return "skip"
    
    return prediction