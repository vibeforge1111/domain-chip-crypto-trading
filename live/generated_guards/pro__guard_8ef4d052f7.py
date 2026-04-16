def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch = features.get('stoch_k', 50)
    
    if prediction == 'long' and vwap_dev > 0.004 and momentum < 0 and stoch > 70:
        return "skip"
    if prediction == 'short' and vwap_dev < -0.004 and momentum > 0 and stoch < 30:
        return "skip"
    
    return prediction