def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch = features.get('stoch_k', 50)
    
    # Skip if price far from VWAP but momentum opposes direction
    if abs(vwap_dev) > 0.04 and momentum * vwap_dev < 0:
        if (vwap_dev > 0 and stoch > 75) or (vwap_dev < 0 and stoch < 25):
            return "skip"
    
    return prediction