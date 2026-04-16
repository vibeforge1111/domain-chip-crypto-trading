def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP (low edge)."""
    if abs(features.get('vwap_deviation', 0)) < 0.005:
        return "skip"
    return prediction