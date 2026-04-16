def guard(features: dict, prediction: str) -> str:
    """Momentum alignment guard - rejects trades where momentum contradicts signal."""
    if prediction == "skip":
        return prediction
    
    momentum = features.get("momentum_score", 0)
    ema_slope = features.get("ema_slope", 0)
    rsi = features.get("rsi_14", 50)
    
    # Skip longs when momentum is negative or EMA is sloping down
    if prediction == "long" and (momentum < -0.1 or ema_slope < -0.01):
        return "skip"
    
    # Skip shorts when momentum is positive or EMA is sloping up
    if prediction == "short" and (momentum > 0.1 or ema_slope > 0.01):
        return "skip"
    
    return prediction