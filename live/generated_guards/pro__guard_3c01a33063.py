def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to VWAP (within 0.5% of price) AND stochastic is neutral
    vwap_dev = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    
    if abs(vwap_dev) < 0.005 and 30 < stoch < 70:
        return "skip"
    return prediction