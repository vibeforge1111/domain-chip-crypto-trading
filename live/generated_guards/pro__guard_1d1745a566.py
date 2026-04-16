def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to fair value with weak momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Filter: if near VWAP (within 0.5%) and momentum is weak, skip
    if abs(vwap_dev) < 0.005 and features.get('momentum_score', 0) < 0.3:
        return "skip"
    return prediction