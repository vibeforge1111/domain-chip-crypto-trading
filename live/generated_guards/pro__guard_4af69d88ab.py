def guard(features: dict, prediction: str) -> str:
    """Filter trades where price is too close to VWAP (fair value)."""
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.002:  # Too close to fair value
        return "skip"
    return prediction