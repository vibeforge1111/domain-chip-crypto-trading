def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP) with weak momentum."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to fair value AND weak momentum
    if vwap_dev < 0.003 and momentum < 0.2:
        return "skip"
    return prediction