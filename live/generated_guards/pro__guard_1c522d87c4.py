def guard(features: dict, prediction: str) -> str:
    """Reject signals when wick bias contradicts the trade direction."""
    if prediction == "skip":
        return prediction
    
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 0)
    range_pct = features.get("range_pct", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Reject small-range candles (potential noise)
    if range_pct < 0.3:
        return "skip"
    
    # Reject low-volume signals (lack of conviction)
    if volume_ratio < 0.7:
        return "skip"
    
    # Reject when wicks dominate body (doji-like indecision)
    if (upper_wick + lower_wick) > 0.6:
        return "skip"
    
    # Wick bias alignment check
    wick_balance = lower_wick - upper_wick
    
    # Long signals need bullish wick bias
    if prediction == "long" and wick_balance < -0.1:
        return "skip"
    
    # Short signals need bearish wick bias
    if prediction == "short" and wick_balance > 0.1:
        return "skip"
    
    return prediction