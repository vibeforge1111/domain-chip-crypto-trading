def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    # Skip if price is within 0.3% of VWAP (no clear edge)
    if abs(vwap_dev) < 0.003:
        return "skip"
    return prediction