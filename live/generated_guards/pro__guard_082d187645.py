def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 0)
    atr_ratio = features.get('atr_ratio', 1)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: both BB and ATR contracted
    true_compression = bb_width < 0.12 and atr_ratio < 0.8
    
    # In compression, reject if stochastic is neutral (no edge)
    if true_compression and 30 <= stoch_k <= 70:
        return "skip"
    
    return prediction