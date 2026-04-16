def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to fair value (VWAP)."""
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Skip if price is within 0.2% of VWAP (no meaningful edge)
    if abs(vwap_deviation) < 0.002:
        return "skip"
    
    return prediction