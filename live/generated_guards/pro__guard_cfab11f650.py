def guard(features: dict, prediction: str) -> str:
    # True compression: low ATR + narrow BB width
    if features['atr_ratio'] > 0.85 or features['bb_width'] > 0.55:
        return "skip"
    
    # Valid compression: bb_pct_b in middle zone (not near extremes)
    if features['bb_pct_b'] < 0.25 or features['bb_pct_b'] > 0.75:
        return "skip"
    
    # Reject if near VWAP extremes (not true compression)
    if abs(features['vwap_deviation']) > 0.015:
        return "skip"
    
    # Skip extreme stochastic readings in compression
    if features['stoch_k'] > 85 or features['stoch_k'] < 15:
        return "skip"
    
    # Valid 2h context: not extended
    if features['rsi_2h'] > 70 or features['rsi_2h'] < 30:
        return "skip"
    
    return prediction