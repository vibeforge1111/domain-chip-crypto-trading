def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip if no crossover imminent (gap too wide)
    if abs(stoch_k - stoch_d) > 5:
        return "skip"
    
    # For longs: need stoch_k below stoch_d (pre-crossover) and oversold zone
    if prediction == "long":
        if stoch_k >= stoch_d or stoch_k > 30:
            return "skip"
    
    # For shorts: need stoch_k above stoch_d (pre-crossover) and overbought zone
    if prediction == "short":
        if stoch_k <= stoch_d or stoch_k < 70:
            return "skip"
    
    return prediction