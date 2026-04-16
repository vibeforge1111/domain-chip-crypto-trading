def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    # Filter trades too close to fair value (low vwap_deviation)
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Filter extreme stochastic readings
    stoch_k = features.get('stoch_k', 50)
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    return prediction