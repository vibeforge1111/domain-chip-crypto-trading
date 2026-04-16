def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Reject trades when price is too close to VWAP (<0.5% deviation)
    if abs(vwap_dev) < 0.005:
        return "skip"
    
    return prediction