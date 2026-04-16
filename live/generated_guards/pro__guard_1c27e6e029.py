def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP (fair value) and extreme stochastic levels."""
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.004:
        return "skip"
    stoch_k = features.get('stoch_k', 50)
    if (prediction == "long" and stoch_k > 85) or (prediction == "short" and stoch_k < 15):
        return "skip"
    return prediction