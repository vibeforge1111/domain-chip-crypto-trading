def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if vwap_deviation and momentum strongly disagree with stochastic confirmation
    if vwap_dev > 0.004 and momentum < -0.25 and stoch_k > 70:
        return "skip"
    if vwap_dev < -0.004 and momentum > 0.25 and stoch_k < 30:
        return "skip"
    
    return prediction