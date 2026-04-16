def guard(features: dict, prediction: str) -> str:
    """Skip if vwap_deviation and momentum_score disagree on direction."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Long: skip if below VWAP with negative momentum
    if prediction == "long" and vwap_dev < -0.005 and momentum < 0:
        return "skip"
    
    # Short: skip if above VWAP with positive momentum
    if prediction == "short" and vwap_dev > 0.005 and momentum > 0:
        return "skip"
    
    return prediction