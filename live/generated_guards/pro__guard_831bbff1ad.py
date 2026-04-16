def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP (no edge) or with extreme stochastic."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if too close to fair value
    if abs(vwap_dev) < 0.003:
        return "skip"
    # Skip if stochastic extreme against trade direction
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    return prediction