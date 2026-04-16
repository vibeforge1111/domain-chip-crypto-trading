def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP or with extreme stochastic readings."""
    # Skip if price is too close to fair value (low directional conviction)
    if abs(features.get('vwap_deviation', 0)) < 0.001:
        return "skip"
    # Skip if stochastic is in extreme territory (potential reversal risk)
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    return prediction