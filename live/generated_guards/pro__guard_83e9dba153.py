def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter longs: skip if price below VWAP with weak/negative momentum
    if prediction == "long" and vwap_dev < -0.003 and momentum < 0.1:
        return "skip"
    
    # Filter shorts: skip if price above VWAP with strong/positive momentum
    if prediction == "short" and vwap_dev > 0.003 and momentum > -0.1:
        return "skip"
    
    # Additional filter: stoch disagreement with direction
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction