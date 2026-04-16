def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Long with price below VWAP and weak momentum
    if prediction == "long" and vwap_dev < -0.002 and momentum < 30:
        return "skip"
    
    # Short with price above VWAP and strong momentum
    if prediction == "short" and vwap_dev > 0.002 and momentum > 70:
        return "skip"
    
    return prediction