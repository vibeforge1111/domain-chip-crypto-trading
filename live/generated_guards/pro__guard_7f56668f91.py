def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 70:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 30:
            return "skip"
    
    return prediction