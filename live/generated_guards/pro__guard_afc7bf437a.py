def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak momentum or low conviction signals."""
    if prediction == "skip":
        return prediction
    
    # Skip if momentum diverges from trend direction
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    
    if prediction == "long" and rsi > 65 and ema_slope < -0.001:
        return "skip"
    if prediction == "short" and rsi < 35 and ema_slope > 0.001:
        return "skip"
    
    # Skip if low volume AND small candle range (no conviction)
    if features.get("volume_ratio", 1) < 0.7 and features.get("range_pct", 0) < 0.5:
        return "skip"
    
    return prediction