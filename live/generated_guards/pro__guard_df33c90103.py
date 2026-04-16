def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    # Skip trades too close to VWAP (low conviction)
    if abs(features.get('vwap_deviation', 0)) < 0.005:
        return "skip"
    return prediction