def guard(features: dict, prediction: str) -> str:
    """Filter trades with indecisive candles during high volatility.
    
    Reject when candle has weak body (high wicks = indecision) AND 
    volatility is elevated (whipsaw risk).
    """
    body_ratio = features.get("body_ratio", 0.5)
    atr_ratio = features.get("atr_ratio", 1.0)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Weak candle + high volatility = reject
    if body_ratio < 0.3 and atr_ratio > 1.3:
        return "skip"
    
    # Very weak candle even with normal volatility
    if body_ratio < 0.2:
        return "skip"
    
    return prediction