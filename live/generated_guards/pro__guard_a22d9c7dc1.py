def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP (fair value lacks directional conviction)."""
    if abs(features.get('vwap_deviation', 0)) < 0.004:
        return "skip"
    return prediction