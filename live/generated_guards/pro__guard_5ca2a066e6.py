def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value)."""
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip if price is within 0.3% of VWAP (too close to fair value)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    return prediction