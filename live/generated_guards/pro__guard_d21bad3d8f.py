def guard(features: dict, prediction: str) -> str:
    # False compression detection: tight BB + low ATR + weak momentum
    if features['bb_width'] < 0.015 and features['atr_ratio'] < 0.5:
        if features['macd_histogram'] <= 0 and features['obv_slope'] <= 0:
            return "skip"
    
    # Skip extended stochastic without momentum confirmation
    if features['stoch_k'] > 85 and features['obv_slope'] <= 0:
        return "skip"
    if features['stoch_k'] < 15 and features['obv_slope'] >= 0:
        return "skip"
    
    return prediction