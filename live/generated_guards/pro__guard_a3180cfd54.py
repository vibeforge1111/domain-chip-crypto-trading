def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and stochastic extremes."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to VWAP fair value (low conviction)
    if abs(vwap_dev) < 0.0015:
        return "skip"
    
    # Skip if both stochastic lines are at extreme levels
    if stoch_k > 80 and stoch_d > 80:
        return "skip"
    if stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction