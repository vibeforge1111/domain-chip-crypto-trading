def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP)."""
    vwap_dev = features.get('vwap_deviation', 0)
    # Skip if price is within 0.15% of VWAP (too close to fair value)
    if abs(vwap_dev) < 0.0015:
        return "skip"
    # Additional filter: skip if stochastic is in extreme zone
    stoch_k = features.get('stoch_k', 50)
    if stoch_k > 80 or stoch_k < 20:
        return "skip"
    return prediction