def guard(features: dict, prediction: str) -> str:
    """Reject trades too close to VWAP fair value (within 0.2%)."""
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    return prediction