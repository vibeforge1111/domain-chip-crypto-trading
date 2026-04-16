def guard(features: dict, prediction: str) -> str:
    # True compression: low BB width + elevated ATR signals volatility expansion coming
    is_compressed = features['bb_width'] < 0.12 and features['atr_ratio'] > 1.15
    
    if not is_compressed:
        return "skip"
    
    # Stochastic confirms momentum direction
    if prediction == 'long' and features['stoch_k'] > features['stoch_d']:
        return prediction
    if prediction == 'short' and features['stoch_k'] < features['stoch_d']:
        return prediction
    
    return "skip"