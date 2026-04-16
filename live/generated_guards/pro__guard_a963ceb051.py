def guard(features: dict, prediction: str) -> str:
    # Reject if large candle but weak volume (institutional disinterest)
    if features['range_pct'] > 1.0 and features['volume_ratio'] < 0.7:
        return "skip"
    
    # Reject if price at extreme BB position with strong trend (reversal risk)
    if features['bb_position'] > 0.9 and features['trend_strength'] > 0.6:
        return "skip"
    if features['bb_position'] < 0.1 and features['trend_strength'] > 0.6:
        return "skip"
    
    # Reject if RSI diverges from trend direction
    if prediction == "long" and features['rsi_14'] < 40:
        return "skip"
    if prediction == "short" and features['rsi_14'] > 60:
        return "skip"
    
    return prediction