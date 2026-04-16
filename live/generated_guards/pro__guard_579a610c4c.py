def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    ema_slope = features.get("ema_slope", 0)
    trend_strength = features.get("trend_strength", 0)
    rsi = features.get("rsi_14", 50)
    bb_pos = features.get("bb_position", 0.5)
    body_ratio = features.get("body_ratio", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Filter: prediction must align with trend direction
    if prediction == "long" and ema_slope < 0.001 and trend_strength < 0.3:
        return "skip"
    if prediction == "short" and ema_slope > -0.001 and trend_strength < 0.3:
        return "skip"
    
    # Filter: weak momentum zone with low volume
    if 45 < rsi < 55 and volume_ratio < 0.8:
        return "skip"
    
    # Filter: exhausted move at extremes
    if body_ratio < 0.2 and (bb_pos > 0.9 or bb_pos < 0.1):
        return "skip"
    
    return prediction