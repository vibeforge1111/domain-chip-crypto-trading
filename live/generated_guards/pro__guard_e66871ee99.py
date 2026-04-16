def guard(features: dict, prediction: str) -> str:
    """Skip longs when momentum is decelerating (weak macd histogram, bearish stoch cross)."""
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long" and (macd < 0.0003 or (stoch_k < stoch_d and rsi_2h > 60)):
        return "skip"
    return prediction