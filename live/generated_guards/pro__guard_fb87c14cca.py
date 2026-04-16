def guard(features: dict, prediction: str) -> str:
    """Reject trades with weak candle conviction and momentum misalignment."""
    body_ratio = features.get("body_ratio", 0)
    rsi_14 = features.get("rsi_14", 50)
    bb_position = features.get("bb_position", 0.5)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Reject if candle is a doji (weak body) AND low volume
    if body_ratio < 0.15 and volume_ratio < 0.8:
        return "skip"
    
    # Reject long signals when RSI overbought (potential reversal)
    if prediction == "long" and rsi_14 > 75:
        return "skip"
    
    # Reject short signals when RSI oversold (potential bounce)
    if prediction == "short" and rsi_14 < 25:
        return "skip"
    
    # Reject when at band extremes with low volume (exhaustion risk)
    if (bb_position > 0.92 or bb_position < 0.08) and volume_ratio < 0.7:
        return "skip"
    
    return prediction