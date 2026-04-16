def guard(features: dict, prediction: str) -> str:
    """Custom guard function filtering on vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Reject when vwap and momentum strongly disagree (opposite signs with significant magnitude)
    if vwap_dev * momentum < -0.015:
        return "skip"
    
    return prediction