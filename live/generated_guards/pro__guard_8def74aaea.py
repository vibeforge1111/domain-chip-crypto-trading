def guard(features: dict, prediction: str) -> str:
    """Filter trades where price is too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if price within 0.3% of VWAP (insufficient directional bias)
    if abs(vwap_dev) < 0.003:
        return "skip"
    return prediction