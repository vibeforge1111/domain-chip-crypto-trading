def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if price is too close to VWAP (within 0.3%) indicating no clear edge
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip if Stochastic is in neutral zone (40-60) suggesting weak momentum
    if 40 < stoch_k < 60:
        return "skip"
    
    return prediction