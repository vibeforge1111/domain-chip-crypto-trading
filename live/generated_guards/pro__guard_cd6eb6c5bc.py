def guard(features: dict, prediction: str) -> str:
    # Reject Bollinger Band squeeze + weak momentum combos
    if features['bb_width'] < 0.3 and features['momentum_score'] < 0.5:
        return "skip"
    
    # Reject conflicting trend direction and candle direction
    if (prediction == "long" and features['lower_wick_ratio'] > 0.5) or \
       (prediction == "short" and features['upper_wick_ratio'] > 0.5):
        return "skip"
    
    # Reject trades when ATR spike without volume confirmation
    if features['atr_ratio'] > 1.8 and features['volume_ratio'] < 0.7:
        return "skip"
    
    return prediction