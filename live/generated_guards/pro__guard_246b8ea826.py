def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to fair value (no edge)."""
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    return prediction