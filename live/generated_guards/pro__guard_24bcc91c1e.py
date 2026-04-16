def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum diverges from trend direction or RSI is extreme."""
    if prediction == "skip":
        return prediction
    
    ema_slope = features.get("ema_slope", 0)
    rsi_14 = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    
    if prediction == "long":
        if ema_slope <= 0:
            return "skip"
        if rsi_14 >= 70:
            return "skip"
        if momentum < 0:
            return "skip"
    
    elif prediction == "short":
        if ema_slope >= 0:
            return "skip"
        if rsi_14 <= 30:
            return "skip"
        if momentum > 0:
            return "skip"
    
    return prediction