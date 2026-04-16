def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Require stochastic crossover alignment with prediction
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Reject if price drifted too far from VWAP (high slippage risk)
    if abs(vwap_dev) > 0.005:
        return "skip"
    
    return prediction