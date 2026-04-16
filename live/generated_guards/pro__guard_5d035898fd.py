def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip if too close to fair value (low VWAP deviation = no edge)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Skip momentum exhaustion at extremes
    if prediction == "long" and stoch_k > 85 and stoch_d > 80:
        return "skip"
    if prediction == "short" and stoch_k < 15 and stoch_d < 20:
        return "skip"
    
    return prediction