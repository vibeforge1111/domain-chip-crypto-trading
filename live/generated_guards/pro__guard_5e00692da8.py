def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is too close to VWAP (no clear deviation from fair value)."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if deviation is too small (< 0.25%) — no clear directional bias from VWAP
    if abs(vwap_dev) < 0.0025:
        return "skip"
    return prediction