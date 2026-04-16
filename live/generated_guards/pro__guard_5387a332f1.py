def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP deviation and momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip when VWAP and momentum strongly disagree
    if vwap_dev > 0.005 and momentum < -0.1:
        return "skip"
    if vwap_dev < -0.005 and momentum > 0.1:
        return "skip"
    
    return prediction