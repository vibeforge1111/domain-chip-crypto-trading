def guard(features: dict, prediction: str) -> str:
    # Skip if too close to VWAP (no directional edge)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Skip if stochastic in extreme territory (potential reversal)
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    return prediction