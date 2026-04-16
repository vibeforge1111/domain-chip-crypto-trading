def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    
    # Reject if price is too close to VWAP and stochastic is neutral
    if vwap_dev < 0.002 and 30 < stoch_k < 70:
        return "skip"
    
    return prediction