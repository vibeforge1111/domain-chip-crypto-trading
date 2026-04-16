def guard(features: dict, prediction: str) -> str:
    """Skip trades where price is too close to VWAP (no edge)."""
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    return prediction