def guard(features: dict, prediction: str) -> str:
    """Reject trades where price is too close to fair value (VWAP)."""
    if abs(features.get('vwap_deviation', 0)) < 0.005:
        return "skip"
    return prediction