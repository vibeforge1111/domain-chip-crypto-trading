def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP (low directional conviction)."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if price within 0.2% of VWAP — insufficient deviation for conviction
    if abs(vwap_dev) < 0.002:
        return "skip"
    return prediction