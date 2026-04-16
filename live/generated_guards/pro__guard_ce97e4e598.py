def guard(features: dict, prediction: str) -> str:
    # True compression: low BB width + ATR confirming stable volatility + balanced oscillators
    if features['bb_width'] > 0.018:
        return "skip"
    
    # Stochastics too far from center suggests directional exhaustion, not true compression
    if abs(features['stoch_k'] - 50) > 30 or abs(features['stoch_d'] - 50) > 30:
        return "skip"
    
    # MACD histogram too strong means momentum, not compression
    if abs(features['macd_histogram']) > 0.0003:
        return "skip"
    
    return prediction