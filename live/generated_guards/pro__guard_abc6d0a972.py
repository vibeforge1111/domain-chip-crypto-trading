def guard(features: dict, prediction: str) -> str:
    # Skip if price at BB extreme with diverging momentum
    if (features['bb_position'] > 0.9 or features['bb_position'] < 0.1) and \
       features['momentum_score'] * (1 - features['bb_position']) < 0:
        return "skip"
    
    # Skip if extreme RSI but weak trend confirmation
    if (features['rsi_14'] > 75 or features['rsi_14'] < 25) and \
       features['trend_strength'] < 0.3:
        return "skip"
    
    # Skip if volume spike without volatility expansion (possible noise)
    if features['volume_ratio'] > 2.5 and features['atr_ratio'] < 1.0:
        return "skip"
    
    return prediction