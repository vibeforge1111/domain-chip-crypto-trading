def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long" and obv_slope < -0.3 and stoch_k < 70:
        return "skip"
    if prediction == "short" and obv_slope > 0.3 and stoch_k > 30:
        return "skip"
    
    return prediction