def guard(features: dict, prediction: str) -> str:
    """Filters trades where momentum and trend are misaligned."""
    if prediction == "skip":
        return prediction
    
    momentum = features.get("momentum_score", 0)
    trend = features.get("trend_strength", 0)
    
    # Longs need both positive; shorts need both negative
    if prediction == "long" and (momentum < 0 or trend < 0):
        return "skip"
    elif prediction == "short" and (momentum > 0 or trend > 0):
        return "skip"
    
    return prediction