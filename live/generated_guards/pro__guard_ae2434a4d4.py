def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value)."""
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.01:
        return "skip"
    return prediction