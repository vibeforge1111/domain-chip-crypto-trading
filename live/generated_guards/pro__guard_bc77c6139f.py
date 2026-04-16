def guard(features: dict, prediction: str) -> str:
    # Skip if price too close to VWAP (< 0.5% deviation) and stochastic neutral
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if abs(vwap_dev) < 0.005 and 25 < stoch_k < 75:
        return "skip"
    return prediction