def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum and candle structure conflict, suggesting reversal risk."""
    
    rsi = features.get("rsi_14", 50)
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body = features.get("body_ratio", 0)
    
    # Long with bearish candle structure (small body, large upper wick) at overbought
    if prediction == "long" and rsi > 70 and upper_wick > 0.25 and body < 0.3:
        return "skip"
    
    # Short with bullish candle structure (small body, large lower wick) at oversold
    if prediction == "short" and rsi < 30 and lower_wick > 0.25 and body < 0.3:
        return "skip"
    
    return prediction