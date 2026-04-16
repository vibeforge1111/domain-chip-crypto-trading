def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    ema_slope = features.get("ema_slope", 0)
    
    # Align with broader trend: longs need bullish 2h RSI, shorts need bearish 2h RSI
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    
    # Additional momentum alignment check using EMA slope
    if prediction == "long" and ema_slope < 0:
        return "skip"
    if prediction == "short" and ema_slope > 0:
        return "skip"
    
    return prediction