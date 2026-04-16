def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (no edge) and extreme stochastic"""
    # Skip if too close to VWAP (within 0.2% - no directional edge)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Skip if stochastic in extreme zone (potential reversal imminent)
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    return prediction