def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    # Reject if price is too close to VWAP (< 0.3% deviation)
    if abs(vwap_dev) < 0.003:
        return "skip"
    return prediction