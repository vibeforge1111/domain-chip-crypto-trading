def guard(features: dict, prediction: str) -> str:
    """Filter trades with poor momentum alignment or weak candle structure."""
    # Reject if momentum strongly contradicts prediction direction
    if prediction == "long" and features['momentum_score'] < -0.25:
        return "skip"
    if prediction == "short" and features['momentum_score'] > 0.25:
        return "skip"
    
    # Reject if candle is mostly wick (low quality setup)
    total_wick = features['upper_wick_ratio'] + features['lower_wick_ratio']
    if total_wick > 0.7:
        return "skip"
    
    # Reject if volume is too low (weak conviction)
    if features['volume_ratio'] < 0.75:
        return "skip"
    
    return prediction