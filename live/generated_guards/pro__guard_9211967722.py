def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if price within 0.2% of VWAP (insufficient edge from fair value)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction