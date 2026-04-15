def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    if vwap_dev < 0.004:  # Too close to fair value, reject
        return "skip"
    return prediction