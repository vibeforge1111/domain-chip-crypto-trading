def guard(features: dict, prediction: str) -> str:
    """Skip when VWAP and momentum strongly disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Reject if VWAP and momentum have opposite signs with meaningful magnitude
    if vwap_dev * momentum < -0.005:
        return "skip"
    
    return prediction