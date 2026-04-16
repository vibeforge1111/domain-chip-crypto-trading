def guard(features: dict, prediction: str) -> str:
    """Reject trades too close to fair value with weak momentum."""
    vwap_dev = abs(features.get("vwap_deviation", 0))
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip if too close to VWAP AND momentum is neutral (both Stoch near 50)
    if vwap_dev < 0.003 and 40 < stoch_k < 60 and 40 < stoch_d < 60:
        return "skip"
    
    return prediction