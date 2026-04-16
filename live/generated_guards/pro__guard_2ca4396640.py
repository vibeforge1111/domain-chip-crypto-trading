def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price is too close to VWAP (<0.2%) with neutral stochastic
    if abs(vwap_dev) < 0.002 and 40 < stoch_k < 60:
        return "skip"
    
    return prediction