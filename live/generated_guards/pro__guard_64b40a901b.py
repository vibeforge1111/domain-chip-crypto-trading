def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value)."""
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    return prediction