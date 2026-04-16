def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    # Skip if too close to VWAP - no clear directional edge
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    return prediction