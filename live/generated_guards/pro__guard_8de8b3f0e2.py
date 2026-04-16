def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Filter when momentum disagrees with VWAP position
    if momentum > 0.15 and vwap_dev < -0.005:
        return "skip"
    if momentum < -0.15 and vwap_dev > 0.005:
        return "skip"
    
    # Additional filter: momentum disagrees with stochastic context
    if momentum > 0.2 and stoch_k < 25:
        return "skip"
    if momentum < -0.2 and stoch_k > 75:
        return "skip"
    
    return prediction