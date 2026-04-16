def guard(features: dict, prediction: str) -> str:
    # Skip trades too close to VWAP (fair value) without momentum confirmation
    vwap_dev = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    
    if abs(vwap_dev) < 0.003 and not (stoch < 20 or stoch > 80):
        return "skip"
    return prediction