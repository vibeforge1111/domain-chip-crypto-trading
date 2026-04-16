def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if significant disagreement between VWAP position and momentum
    if abs(vwap_dev) > 0.005 and abs(momentum) > 0.1:
        if (vwap_dev < 0 and momentum > 0) or (vwap_dev > 0 and momentum < 0):
            return 'skip'
    
    return prediction