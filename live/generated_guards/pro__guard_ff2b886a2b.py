def guard(features: dict, prediction: str) -> str:
    # Momentum-volume divergence: reject if momentum is strong but volume is weak (fakeout)
    if features['momentum_score'] > 0.4 and features['volume_ratio'] < 0.6:
        return "skip"
    if features['momentum_score'] < -0.4 and features['volume_ratio'] < 0.6:
        return "skip"
    
    # Wick-body imbalance: reject if large wick on opposite side of prediction
    if prediction == "long" and features['lower_wick_ratio'] > features['body_ratio'] * 1.5:
        return "skip"
    if prediction == "short" and features['upper_wick_ratio'] > features['body_ratio'] * 1.5:
        return "skip"
    
    # Stochastic exhaustion: reject if both stochastic and RSI are extreme together
    if features['stoch_k'] > 85 and features['rsi_14'] > 70:
        return "skip"
    if features['stoch_k'] < 15 and features['rsi_14'] < 30:
        return "skip"
    
    return prediction