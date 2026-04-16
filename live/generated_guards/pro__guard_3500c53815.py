def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to VWAP and stochastic shows no conviction
    if abs(vwap_dev) < 0.002 and stoch_k < 70:
        return "skip"
    
    return prediction