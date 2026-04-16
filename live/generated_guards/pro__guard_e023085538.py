def guard(features: dict, prediction: str) -> str:
    # Skip if price too close to VWAP (no edge)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    # Skip if stochastic in extreme reversal zones
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    return prediction