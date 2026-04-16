def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to VWAP (no directional conviction)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip if stochastic is divergent or extreme
    if abs(stoch_k - stoch_d) > 20:
        return "skip"
    if stoch_k > 90 or stoch_k < 10:
        return "skip"
    
    return prediction