def guard(features: dict, prediction: str) -> str:
    # Filter: Extreme RSI + high volatility = potential reversal, skip
    if (features['rsi_14'] < 30 or features['rsi_14'] > 70) and features['atr_ratio'] > 1.3:
        return "skip"
    
    # Filter: Dominant wicks signal indecision/weak momentum
    if features['upper_wick_ratio'] + features['lower_wick_ratio'] > features['body_ratio'] * 2:
        return "skip"
    
    # Filter: Extreme BB position with weak momentum signals exhaustion
    if (features['bb_position'] > 0.9 or features['bb_position'] < 0.1) and features['momentum_score'] < 0.3:
        return "skip"
    
    return prediction