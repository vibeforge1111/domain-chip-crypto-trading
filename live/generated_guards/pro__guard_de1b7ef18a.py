def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_deviation = features.get('vwap_deviation', 0)
    if abs(vwap_deviation) < 0.0025:
        return "skip"
    return prediction