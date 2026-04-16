def guard(features: dict, prediction: str) -> str:
    """Reject trades with weak candle structure conflicting with trend/momentum."""
    if prediction == "skip":
        return prediction
    
    # Reject if candle has weak structure (large wicks, small body)
    candle_quality = features.get("body_ratio", 0) - features.get("upper_wick_ratio", 0) - features.get("lower_wick_ratio", 0)
    weak_candle = candle_quality < 0.1
    
    # Check trend/momentum alignment
    trend_ok = features.get("trend_strength", 0) > 0.3 and features.get("momentum_score", 0) > 0
    volume_ok = features.get("volume_ratio", 0) > 0.7
    
    # Reject if weak candle AND no trend/volume support
    if weak_candle and not (trend_ok and volume_ok):
        return "skip"
    
    return prediction