def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between vwap_deviation and momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Price extended from VWAP but momentum/stochastic contradict direction
    if vwap_dev > 0.004 and momentum < 0.35 and stoch < 45:
        return "skip"
    if vwap_dev < -0.004 and momentum > 0.65 and stoch > 55:
        return "skip"
    
    return prediction