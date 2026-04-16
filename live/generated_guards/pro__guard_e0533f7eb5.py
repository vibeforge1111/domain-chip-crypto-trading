def guard(features: dict, prediction: str) -> str:
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_d = features.get('stoch_d', 50)
    
    if vwap_dev < 0.003:
        return "skip"
    
    if prediction == "long" and stoch_d < 25:
        return "skip"
    if prediction == "short" and stoch_d > 75:
        return "skip"
    
    return prediction