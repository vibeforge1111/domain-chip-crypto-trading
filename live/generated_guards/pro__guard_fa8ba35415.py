def guard(features: dict, prediction: str) -> str:
    # Skip if price too close to fair value (VWAP) AND in extreme stoch territory
    vwap_dev = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    
    if abs(vwap_dev) < 0.003 and (stoch > 80 or stoch < 20):
        return "skip"
    return prediction