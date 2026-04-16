def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if price within 0.2% of VWAP (too close to fair value)
    if abs(vwap_deviation) < 0.002:
        return "skip"
    
    # Additional filter: skip momentum extremes near VWAP
    if abs(vwap_deviation) < 0.005 and (stoch_k > 80 or stoch_k < 20):
        return "skip"
    
    return prediction