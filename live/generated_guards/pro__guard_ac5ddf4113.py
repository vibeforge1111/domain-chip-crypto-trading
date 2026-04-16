def guard(features: dict, prediction: str) -> str:
    """Reject trades when price is too close to VWAP (low directional bias)."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price is too close to fair value (low directional bias)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip if stochastic at extreme reversal zones
    if stoch_k > 80 or stoch_k < 20:
        return "skip"
    
    return prediction