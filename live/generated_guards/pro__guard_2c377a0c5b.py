def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and momentum extremes."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to VWAP (no edge)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip counter-trend trades at momentum extremes
    if prediction == "long" and stoch_k > 80 and stoch_d > 75:
        return "skip"
    if prediction == "short" and stoch_k < 20 and stoch_d < 25:
        return "skip"
    
    return prediction