def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    # Skip if too close to VWAP (within 0.2% of price)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction