def guard(features: dict, prediction: str) -> str:
    # Skip if strong wick imbalance in weak trend (potential reversal trap)
    wick_imbalance = abs(features['upper_wick_ratio'] - features['lower_wick_ratio'])
    if wick_imbalance > 0.55 and features['trend_strength'] < 0.35:
        return "skip"
    
    # Skip if candle is mostly wick (doji/exhaustion pattern)
    if features['body_ratio'] < 0.25:
        return "skip"
    
    # Skip if low volume confirms large range (low conviction move)
    if features['volume_ratio'] < 0.6 and features['range_pct'] > 1.5:
        return "skip"
    
    return prediction