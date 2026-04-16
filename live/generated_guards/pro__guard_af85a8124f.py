def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value) with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.0015:
        return "skip"
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k > 75:
        return "skip"
    if prediction == "short" and stoch_k < 25:
        return "skip"
    return prediction