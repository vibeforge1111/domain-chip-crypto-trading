def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation and stochastic."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price too close to fair value (|vwap_deviation| < 0.003)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip if stochastic in neutral zone (40-60)
    if 40 < stoch_k < 60:
        return "skip"
    
    return prediction