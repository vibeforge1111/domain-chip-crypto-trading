def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum divergence (RSI vs EMA slope conflict)."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    momentum_score = features.get("momentum_score", 0)
    
    # Bullish momentum divergence: price rising but weakening
    if ema_slope > 0 and rsi < 60 and momentum_score < 0.4:
        return "skip"
    
    # Bearish momentum divergence: price falling but strengthening  
    if ema_slope < 0 and rsi > 40 and momentum_score > 0.6:
        return "skip"
    
    return prediction