def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (no edge) or with extreme stochastic."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to fair value (< 0.2% from VWAP)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Skip if stochastic is extreme (reversal risk)
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction