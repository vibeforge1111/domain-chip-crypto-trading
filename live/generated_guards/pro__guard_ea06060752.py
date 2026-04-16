def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to VWAP (fair value) with neutral stochastic
    if vwap_dev < 0.001 and 30 < stoch_k < 70:
        return "skip"
    
    return prediction