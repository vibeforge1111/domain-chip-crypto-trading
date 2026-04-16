def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP (fair value equilibrium zone)."""
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.004:  # Within 0.4% of fair value - low edge
        return "skip"
    return prediction