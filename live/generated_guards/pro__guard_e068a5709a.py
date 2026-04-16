def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    # Skip if price is within 0.2% of fair value (VWAP)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    return prediction