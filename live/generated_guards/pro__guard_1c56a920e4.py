def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if price is too close to fair value
    if abs(vwap_dev) < 0.005:
        return "skip"
    
    # Validate momentum alignment with trade direction
    if prediction == "long" and stoch_k < 25:
        return "skip"
    if prediction == "short" and stoch_k > 75:
        return "skip"
    
    return prediction