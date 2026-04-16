def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if deviation from VWAP is too small (<0.15%)
    if abs(vwap_dev) < 0.0015:
        return "skip"
    return prediction