def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip when vwap and momentum disagree (price extended but momentum fading)
    if vwap_dev > 0.003 and momentum < -0.15 and stoch_k > 70:
        return "skip"
    if vwap_dev < -0.003 and momentum > 0.15 and stoch_k < 30:
        return "skip"
    
    return prediction