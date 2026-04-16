def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if VWAP and momentum disagree strongly
    if prediction == 'long':
        if vwap_dev < -0.005 and momentum > 0.2:
            return "skip"
        if stoch_k > 80 and momentum < 0:
            return "skip"
    elif prediction == 'short':
        if vwap_dev > 0.005 and momentum < -0.2:
            return "skip"
        if stoch_k < 20 and momentum > 0:
            return "skip"
    
    return prediction