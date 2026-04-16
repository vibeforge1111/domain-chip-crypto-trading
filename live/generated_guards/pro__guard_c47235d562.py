def guard(features: dict, prediction: str) -> str:
    """Filters trades with reversal-prone candle patterns (large opposing wick)."""
    ema_slope = features.get("ema_slope", 0)
    upper_wick_ratio = features.get("upper_wick_ratio", 0)
    lower_wick_ratio = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 0.5)
    
    # Skip weak candles with minimal body (indecision)
    if body_ratio < 0.3:
        return "skip"
    
    # Long trades: reject if large upper wick in uptrend (reversal signal)
    if prediction == "long" and ema_slope > 0 and upper_wick_ratio > 0.5:
        return "skip"
    
    # Short trades: reject if large lower wick in downtrend (reversal signal)
    if prediction == "short" and ema_slope < 0 and lower_wick_ratio > 0.5:
        return "skip"
    
    return prediction