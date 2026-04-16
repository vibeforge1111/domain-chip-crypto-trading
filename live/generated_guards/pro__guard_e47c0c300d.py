def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to VWAP (within 0.2% of price)
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.002:
        return "skip"
    # Also skip if in extreme stochastic territory with weak VWAP confirmation
    stoch_k = features.get('stoch_k', 50)
    if (stoch_k > 80 or stoch_k < 20) and abs(vwap_dev) < 0.005:
        return "skip"
    return prediction