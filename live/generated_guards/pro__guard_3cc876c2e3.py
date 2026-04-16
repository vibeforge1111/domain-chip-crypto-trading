def guard(features: dict, prediction: str) -> str:
    """Squeeze breakout guard - filters trades during low volatility periods with weak momentum."""
    bb_width = features.get("bb_width", 1.0)
    volume_ratio = features.get("volume_ratio", 1.0)
    momentum_score = features.get("momentum_score", 0.0)
    ema_slope = features.get("ema_slope", 0.0)
    
    # Skip if Bollinger Band squeeze (low volatility) AND weak momentum
    if bb_width < 0.15 and abs(momentum_score) < 0.3:
        return "skip"
    
    # Skip if low volume during breakout attempt
    if bb_width > 0.3 and volume_ratio < 0.8:
        return "skip"
    
    # Momentum-direction alignment filter
    if prediction == "long" and ema_slope < -0.001 and momentum_score < -0.2:
        return "skip"
    if prediction == "short" and ema_slope > 0.001 and momentum_score > 0.2:
        return "skip"
    
    return prediction