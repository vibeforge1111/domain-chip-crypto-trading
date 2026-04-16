def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value)."""
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.003:  # within 0.3% of fair value
        return "skip"
    return prediction