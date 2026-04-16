def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    vwap_deviation = features.get('vwap_deviation', 0)
    # Skip if price is within 0.3% of VWAP (not enough edge)
    if abs(vwap_deviation) < 0.003:
        return "skip"
    return prediction