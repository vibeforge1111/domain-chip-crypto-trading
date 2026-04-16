def guard(features: dict, prediction: str) -> str:
    # Filter trades too close to fair value (low opportunity)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    
    # Filter if stochastic is in neutral zone (indecision)
    stoch_k = features.get('stoch_k', 50)
    if 25 < stoch_k < 75:
        return "skip"
    
    return prediction