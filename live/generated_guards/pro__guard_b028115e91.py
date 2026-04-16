def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == "long" and (stoch_k <= stoch_d or obv_slope <= 0):
        return "skip"
    if prediction == "short" and (stoch_k >= stoch_d or obv_slope >= 0):
        return "skip"
    
    return prediction