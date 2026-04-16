def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP (choppy zone)."""
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction