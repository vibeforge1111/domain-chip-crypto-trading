def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter: disagreement between vwap position and momentum direction
    if vwap_dev > 0.02 and momentum < -0.2:
        return "skip"
    if vwap_dev < -0.02 and momentum > 0.2:
        return "skip"
    
    # Filter: stochastic confirms momentum, contradicts prediction
    if prediction == "long" and stoch_k < 25:
        return "skip"
    if prediction == "short" and stoch_k > 75:
        return "skip"
    
    return prediction