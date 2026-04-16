def guard(features: dict, prediction: str) -> str:
    """Reject trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if meaningful VWAP deviation contradicts momentum direction
    if abs(vwap_dev) > 0.008 and vwap_dev * momentum < 0:
        return "skip"
    
    return prediction