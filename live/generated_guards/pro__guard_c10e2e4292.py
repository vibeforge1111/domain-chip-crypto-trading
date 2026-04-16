def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction