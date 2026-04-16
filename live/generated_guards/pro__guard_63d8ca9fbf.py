def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum indicators conflict with trend direction."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    momentum_score = features.get("momentum_score", 0)
    
    # Reject longs when RSI below 45 in downtrend with negative momentum
    if prediction == "long" and rsi < 45 and ema_slope < 0 and momentum_score < 0:
        return "skip"
    
    # Reject shorts when RSI above 55 in uptrend with positive momentum  
    if prediction == "short" and rsi > 55 and ema_slope > 0 and momentum_score > 0:
        return "skip"
    
    return prediction