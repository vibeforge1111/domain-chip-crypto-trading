def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum conflicts with trend direction."""
    ema_slope = features.get("ema_slope", 0)
    momentum_score = features.get("momentum_score", 0)
    
    # Only skip if momentum opposes trend significantly
    if prediction == "long" and ema_slope > 0 and momentum_score < -0.3:
        return "skip"
    if prediction == "short" and ema_slope < 0 and momentum_score > 0.3:
        return "skip"
    
    return prediction