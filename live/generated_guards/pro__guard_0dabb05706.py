def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio and BB width."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: both volatility measures are low
    is_compressed = atr_ratio < 0.7 and bb_width < 0.3
    
    if is_compressed:
        # False compression when stochastic is extreme during squeeze
        if stoch_k > 85 or stoch_k < 15:
            return "skip"
        # False compression when wider timeframe RSI is extreme
        if rsi_2h > 75 or rsi_2h < 25:
            return "skip"
    
    return prediction