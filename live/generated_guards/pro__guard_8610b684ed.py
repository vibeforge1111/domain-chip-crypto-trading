def guard(features: dict, prediction: str) -> str:
    """Reject trades where candle wicks suggest reversal, not continuation."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 0)
    rsi = features.get("rsi_14", 50)
    trend = features.get("trend_strength", 0.5)
    
    # Large wick + small body = rejection candle (weak conviction)
    if body_ratio < 0.3 and (upper_wick > 0.4 or lower_wick > 0.4):
        return "skip"
    
    # Long signal with large upper wick = likely bearish rejection
    if prediction == "long" and upper_wick > 0.5:
        return "skip"
    
    # Short signal with large lower wick = likely bullish rejection  
    if prediction == "short" and lower_wick > 0.5:
        return "skip"
    
    # RSI extreme + weak trend = low probability
    if rsi > 75 and trend < 0.3:
        return "skip"
    if rsi < 25 and trend < 0.3:
        return "skip"
    
    return prediction