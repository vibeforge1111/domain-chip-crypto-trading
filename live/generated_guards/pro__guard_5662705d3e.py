def guard(features: dict, prediction: str) -> str:
    """Filter signals based on candle indecision, volume confirmation, and momentum alignment."""
    # Skip if candle shows indecision (wicks on both sides, small body)
    if features['upper_wick_ratio'] > 0.3 and features['lower_wick_ratio'] > 0.3 and features['body_ratio'] < 0.3:
        return "skip"
    
    # Skip if significant price move without volume confirmation
    if features['range_pct'] > 1.5 and features['volume_ratio'] < 0.7:
        return "skip"
    
    # Skip if RSI in extreme zone but trend strength is weak (divergence signal)
    if (features['rsi_14'] > 70 or features['rsi_14'] < 30) and features['trend_strength'] < 0.3:
        return "skip"
    
    return prediction