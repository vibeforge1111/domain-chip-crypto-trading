def guard(features: dict, prediction: str) -> str:
    # Skip trades too close to VWAP (within 0.2% - low edge)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Additional momentum filter - skip overextended entries
    stoch_k = features.get('stoch_k', 50)
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    return prediction