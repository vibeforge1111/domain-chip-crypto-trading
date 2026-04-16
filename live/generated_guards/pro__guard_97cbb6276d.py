def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if price is too close to VWAP (< 0.3% away)
    if abs(vwap_dev) < 0.003:
        return "skip"
    return prediction