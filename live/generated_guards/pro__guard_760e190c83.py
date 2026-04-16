def guard(features: dict, prediction: str) -> str:
    # Detect compression: low ATR and narrow BB
    is_compressed = features.get('atr_ratio', 1) < 0.6 and features.get('bb_width', 1) < 0.4
    
    if not is_compressed:
        return prediction
    
    # During compression, avoid extreme stochastic (false breakout risk)
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    
    # During compression, avoid extreme RSI
    if features.get('rsi_14', 50) > 72 or features.get('rsi_14', 50) < 28:
        return "skip"
    
    # During compression, VWAP deviation should be moderate
    if abs(features.get('vwap_deviation', 0)) > 0.015:
        return "skip"
    
    return prediction