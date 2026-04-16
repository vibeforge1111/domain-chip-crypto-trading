def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Long signals: reject if price below VWAP while momentum is negative
    if prediction == "long":
        if vwap_dev < -0.005 and momentum < -0.1:
            return "skip"
    
    # Short signals: reject if price above VWAP while momentum is positive
    if prediction == "short":
        if vwap_dev > 0.005 and momentum > 0.1:
            return "skip"
    
    return prediction