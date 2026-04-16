def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression to avoid false breakouts."""
    # True compression: both low ATR and low BB width
    in_compression = features['atr_ratio'] < 0.7 and features['bb_width'] < 0.6
    
    if in_compression and prediction != "skip":
        # During compression, reject if stoch is at extremes (likely reversal)
        if features['stoch_k'] > 80 or features['stoch_k'] < 20:
            return "skip"
        # During compression, require aligned momentum
        if features['macd_histogram'] < 0 and prediction == "long":
            return "skip"
        if features['macd_histogram'] > 0 and prediction == "short":
            return "skip"
    return prediction