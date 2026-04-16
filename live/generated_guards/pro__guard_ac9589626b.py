def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    if 40 < features.get('stoch_k', 50) < 60 and abs(features.get('vwap_deviation', 0)) < 0.005:
        return "skip"
    return prediction