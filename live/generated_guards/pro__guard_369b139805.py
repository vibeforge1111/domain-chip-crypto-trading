def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum diverges from trend strength."""
    if prediction == "skip":
        return prediction
    
    momentum = features.get("momentum_score", 0)
    trend = features.get("trend_strength", 0)
    
    # Skip trades where momentum opposes trend direction
    if prediction == "long" and momentum < -0.3 and trend < -0.2:
        return "skip"
    if prediction == "short" and momentum > 0.3 and trend > 0.2:
        return "skip"
    
    return prediction