def guard(features: dict, prediction: str) -> str:
    """VWAP proximity guard - skip when price too close to fair value with momentum conflicts."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to VWAP AND stochastic shows weak momentum
    if vwap_dev < 0.003 and stoch_k < 40:
        return "skip"
    
    # Skip if near VWAP with bearish stochastic divergence
    if vwap_dev < 0.005 and stoch_k < stoch_d:
        return "skip"
    
    return prediction