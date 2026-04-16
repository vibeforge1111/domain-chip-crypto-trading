def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value)."""
    vwap_dev = abs(features.get("vwap_deviation", 0))
    if vwap_dev < 0.005:  # Within 0.5% of fair value - no edge
        return "skip"
    return prediction