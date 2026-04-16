def guard(features: dict, prediction: str) -> str:
    # Skip if too close to VWAP (no clear directional signal)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Skip if in extreme stoch territory (reversal risk)
    if features.get('stoch_k', 50) > 80 or features.get('stoch_k', 50) < 20:
        return "skip"
    return prediction