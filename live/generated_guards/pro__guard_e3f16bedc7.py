def guard(features: dict, prediction: str) -> str:
    """Skip when vwap_deviation and momentum_score strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price far from VWAP but momentum contradicts direction
    if vwap_dev * momentum < -0.0008 and abs(vwap_dev) > 0.008 and abs(momentum) > 0.2:
        return "skip"
    
    return prediction