def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to fair value (VWAP) for better risk/reward."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to VWAP (within 0.3% - low conviction)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Additional: avoid longs at extreme stochastic overbought
    if prediction == "long" and stoch_k > 85:
        return "skip"
    
    return prediction