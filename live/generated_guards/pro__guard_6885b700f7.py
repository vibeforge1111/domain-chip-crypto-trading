def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_deviation = features.get('vwap_deviation', 0)
    # Skip if price is too close to fair value (no edge)
    if abs(vwap_deviation) < 0.001:  # less than 0.1% from VWAP
        return "skip"
    return prediction