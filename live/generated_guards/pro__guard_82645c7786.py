def guard(features: dict, prediction: str) -> str:
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    # Skip if price too close to fair value (low edge)
    if abs(vwap_deviation) < 0.001:
        return "skip"
    # Skip if stochastic in extreme zone
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    return prediction