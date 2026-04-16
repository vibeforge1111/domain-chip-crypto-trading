def guard(features: dict, prediction: str) -> str:
    # Filter trades too close to fair value (weak directional signal)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    # Reject neutral stochastic readings
    if 35 < features.get('stoch_k', 50) < 65:
        return "skip"
    return prediction