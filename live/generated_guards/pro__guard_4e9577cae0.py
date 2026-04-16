def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch = features.get("stoch_k", 50)
    
    # Long signal but price far below VWAP with weak/negative momentum
    if prediction == "long" and vwap_dev < -0.005 and momentum < 0.1:
        return "skip"
    
    # Short signal but price far above VWAP with weak/positive momentum
    if prediction == "short" and vwap_dev > 0.005 and momentum > -0.1:
        return "skip"
    
    # Extra filter: extreme stoch position without momentum confirmation
    if prediction == "long" and stoch < 25:
        return "skip"
    if prediction == "short" and stoch > 75:
        return "skip"
    
    return prediction