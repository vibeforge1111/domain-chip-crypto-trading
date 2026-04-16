def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if prediction == "long":
        if stoch_k <= stoch_d or stoch_k > 70:
            return "skip"
        if bb_pct_b > 0.85:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d or stoch_k < 30:
            return "skip"
        if bb_pct_b < 0.15:
            return "skip"
    
    return prediction