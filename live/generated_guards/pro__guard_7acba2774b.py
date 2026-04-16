def guard(features: dict, prediction: str) -> str:
    """Filter signals with suspicious candle structure or momentum divergence."""
    # Reject weak signals: small body + low volume = indecision
    if features['body_ratio'] < 0.2 and features['volume_ratio'] < 0.8:
        return "skip"
    
    # Reject long setups with dominant upper wick (selling pressure)
    if prediction == "long" and features['upper_wick_ratio'] > 0.6:
        return "skip"
    
    # Reject short setups with dominant lower wick (buying pressure)
    if prediction == "short" and features['lower_wick_ratio'] > 0.6:
        return "skip"
    
    # Skip if momentum contradicts trend direction
    if prediction == "long" and features['momentum_score'] < -0.3:
        return "skip"
    if prediction == "short" and features['momentum_score'] > 0.3:
        return "skip"
    
    return prediction