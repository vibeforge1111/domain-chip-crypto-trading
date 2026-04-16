def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to fair value with momentum exhaustion."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if no VWAP edge and at stochastic extremes
    if abs(vwap_dev) < 0.005 and (stoch_k > 85 or stoch_k < 15):
        return "skip"
    return prediction