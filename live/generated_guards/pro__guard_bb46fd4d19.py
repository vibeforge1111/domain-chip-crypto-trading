def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to VWAP (within 0.2%) - no clear directional bias
    if vwap_dev < 0.002:
        return "skip"
    
    # Skip if Stochastic is in extreme zone
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction