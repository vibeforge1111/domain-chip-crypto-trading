def guard(features: dict, prediction: str) -> str:
    """Filter signals where trend strength and EMA slope are misaligned."""
    ema_slope = features.get('ema_slope', 0)
    trend_strength = features.get('trend_strength', 0)
    
    # Skip if trend strength is moderate-strong but EMA slope contradicts
    if trend_strength > 0.3 and abs(ema_slope) < 0.001:
        return "skip"
    
    # Skip if strong trend but EMA moves opposite direction
    if trend_strength > 0.5 and (ema_slope * (1 if prediction == "long" else -1)) < 0:
        return "skip"
    
    return prediction