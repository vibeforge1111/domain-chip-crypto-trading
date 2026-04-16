def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if indicators strongly disagree
    # Price extended above VWAP but losing momentum
    if vwap_dev > 0.008 and momentum < -0.1:
        return "skip"
    
    # Price below VWAP but momentum not confirming
    if vwap_dev < -0.008 and momentum > 0.1:
        return "skip"
    
    return prediction