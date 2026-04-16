def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    if prediction == "long" and stoch_k < 20:
        return "skip"
    if prediction == "short" and stoch_k > 80:
        return "skip"
    
    return prediction