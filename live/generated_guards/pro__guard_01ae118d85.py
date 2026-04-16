def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = abs(features.get("vwap_deviation", 0))
    
    # Skip if price is within 0.2% of VWAP (too close to fair value)
    if vwap_dev < 0.002:
        return "skip"
    
    return prediction