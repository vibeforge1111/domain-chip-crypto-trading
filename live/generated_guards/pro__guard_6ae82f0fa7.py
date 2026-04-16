def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value)."""
    vwap_deviation = features.get('vwap_deviation', 0)
    if abs(vwap_deviation) < 0.002:
        return "skip"
    return prediction