def guard(features: dict, prediction: str) -> str:
    """Custom guard function that filters trades too close to fair value using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction