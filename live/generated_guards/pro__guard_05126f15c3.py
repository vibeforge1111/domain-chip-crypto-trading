def guard(features: dict, prediction: str) -> str:
    """Filter trades with wick imbalance lacking volume confirmation or RSI extremes without momentum."""
    # Skip if strong wick imbalance without volume confirmation
    wick_diff = abs(features['upper_wick_ratio'] - features['lower_wick_ratio'])
    if wick_diff > 0.4 and features['volume_ratio'] < 0.7:
        return "skip"
    
    # Skip if RSI at extreme without momentum support
    if (features['rsi_14'] > 75 or features['rsi_14'] < 25) and features['momentum_score'] < 0.3:
        return "skip"
    
    return prediction