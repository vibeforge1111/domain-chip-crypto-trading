def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak trend or momentum exhaustion."""
    # Skip if trend strength is weak (no clear direction)
    if features.get('trend_strength', 0) < 0.3:
        return "skip"
    
    # Skip if RSI in extreme zone (reversal risk)
    rsi = features.get('rsi_14', 50)
    if prediction == "long" and rsi > 72:
        return "skip"
    if prediction == "short" and rsi < 28:
        return "skip"
    
    # Skip if EMA slope contradicts prediction
    ema_slope = features.get('ema_slope', 0)
    if prediction == "long" and ema_slope < 0:
        return "skip"
    if prediction == "short" and ema_slope > 0:
        return "skip"
    
    return prediction