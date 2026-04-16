def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation and momentum score strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if VWAP and momentum strongly disagree (opposite signs with magnitude)
    if vwap_dev * momentum < -0.01:
        return "skip"
    
    return prediction