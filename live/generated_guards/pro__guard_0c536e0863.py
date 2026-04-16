def guard(features: dict, prediction: str) -> str:
    """Reject signals where VWAP deviation and momentum score strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if significant VWAP deviation contradicts momentum/stoch direction
    if vwap_dev > 0.01 and momentum < 0 and stoch_k < 40:
        return "skip"
    if vwap_dev < -0.01 and momentum > 0 and stoch_k > 60:
        return "skip"
    
    return prediction