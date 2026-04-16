def guard(features: dict, prediction: str) -> str:
    """Filter trades on candle quality and trend alignment."""
    body_ratio = features.get("body_ratio", 0)
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    ema_slope = features.get("ema_slope", 0)
    trend_strength = features.get("trend_strength", 0)
    
    # Strong body indicates conviction
    if body_ratio < 0.4:
        return "skip"
    
    # For longs: prefer bullish candles + uptrend
    if prediction == "long":
        if lower_wick > 0.3:  # Reject if too much lower wick
            return "skip"
        if ema_slope < 0 and trend_strength > 0.5:  # Reject counter-trend
            return "skip"
    
    # For shorts: prefer bearish candles + downtrend
    if prediction == "short":
        if upper_wick > 0.3:  # Reject if too much upper wick
            return "skip"
        if ema_slope > 0 and trend_strength > 0.5:  # Reject counter-trend
            return "skip"
    
    return prediction