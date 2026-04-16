def guard(features: dict, prediction: str) -> str:
    """Reject trades too close to fair value or at stochastic extremes."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if abs(vwap_dev) < 0.002:
        return "skip"
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    return prediction