def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Reject long signals when price below VWAP with negative momentum
    if prediction == "long" and vwap_dev < -0.005 and momentum < -0.25:
        return "skip"
    
    # Reject short signals when price above VWAP with positive momentum
    if prediction == "short" and vwap_dev > 0.005 and momentum > 0.25:
        return "skip"
    
    return prediction