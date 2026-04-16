def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP (no edge from fair value)."""
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip if price within 0.2% of VWAP (no meaningful deviation from fair value)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction