def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if within 0.15% of VWAP (no clear directional bias)
    if abs(vwap_dev) < 0.0015:
        return 'skip'
    return prediction