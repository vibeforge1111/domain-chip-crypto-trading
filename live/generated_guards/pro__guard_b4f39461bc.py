def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if price is within 0.2% of VWAP (no clear directional pressure)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction