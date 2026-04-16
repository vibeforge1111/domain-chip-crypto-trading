def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    # Skip if price is within 0.5% of VWAP (no edge)
    if abs(features.get('vwap_deviation', 0)) < 0.005:
        return "skip"
    return prediction