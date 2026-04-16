def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip trades too close to fair value (VWAP) - no edge
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction