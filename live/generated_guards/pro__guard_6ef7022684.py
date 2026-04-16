def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    vwap_deviation = features.get('vwap_deviation', 0)
    # Filter trades too close to fair value (VWAP)
    if abs(vwap_deviation) < 0.002:
        return "skip"
    # Filter extreme stochastic readings
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    return prediction