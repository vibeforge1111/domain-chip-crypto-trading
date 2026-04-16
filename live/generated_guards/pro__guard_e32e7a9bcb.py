def guard(features: dict, prediction: str) -> str:
    # Skip if too close to VWAP (no edge from fair value)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    # Skip if stochastic extreme (reversal risk)
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    return prediction