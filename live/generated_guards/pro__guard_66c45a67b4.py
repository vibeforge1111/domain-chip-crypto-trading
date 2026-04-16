def guard(features: dict, prediction: str) -> str:
    """Guard function filtering trades based on BB position + trend alignment + RSI."""
    if prediction == "skip":
        return prediction
    
    bb_pos = features.get("bb_position", 0.5)
    ema_slope = features.get("ema_slope", 0)
    rsi = features.get("rsi_14", 50)
    body_ratio = features.get("body_ratio", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Reject if candle has very small body (potential reversal) and extreme BB position
    if body_ratio < 0.2 and (bb_pos < 0.15 or bb_pos > 0.85):
        return "skip"
    
    # Reject if price is at extreme BB and RSI confirms overbought/oversold
    if bb_pos > 0.9 and rsi > 70:
        return "skip"
    if bb_pos < 0.1 and rsi < 30:
        return "skip"
    
    # Reject if moving against strong trend with low volume confirmation
    if abs(ema_slope) > 0.05:
        if (prediction == "long" and ema_slope < -0.02 and volume_ratio < 1.3):
            return "skip"
        if (prediction == "short" and ema_slope > 0.02 and volume_ratio < 1.3):
            return "skip"
    
    return prediction