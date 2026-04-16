def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    if vwap_dev < 0.002:
        return "skip"
    return prediction