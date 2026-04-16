def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using rsi_2h and avoid extreme momentum."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # For longs: need supportive broader trend (rsi_2h >= 40) and not extreme oversold
    if prediction == "long" and (rsi_2h < 40 or stoch_k < 15):
        return "skip"
    
    # For shorts: need non-bullish broader trend (rsi_2h <= 60) and not extreme overbought
    if prediction == "short" and (rsi_2h > 60 or stoch_k > 85):
        return "skip"
    
    return prediction