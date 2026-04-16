def guard(features: dict, prediction: str) -> str:
    # Skip trades too close to fair value (VWAP)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Skip extreme stochastic readings
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    return prediction