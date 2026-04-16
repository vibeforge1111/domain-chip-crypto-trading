def guard(features: dict, prediction: str) -> str:
    """Filter trades when VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if strong disagreement: price far below VWAP but momentum positive, or vice versa
    if vwap_dev < -0.015 and momentum > 0.4:
        return "skip"
    if vwap_dev > 0.015 and momentum < -0.4:
        return "skip"
    
    return prediction