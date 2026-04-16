def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Reject if within 0.3% of VWAP (no meaningful edge)
    if abs(vwap_dev) < 0.003:
        return "skip"
    return prediction