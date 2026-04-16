def guard(features: dict, prediction: str) -> str:
    """Reject trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.0025:
        return "skip"
    return prediction