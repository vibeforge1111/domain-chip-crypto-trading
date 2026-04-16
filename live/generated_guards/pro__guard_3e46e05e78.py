def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Require bullish crossover: stoch_k must be above stoch_d
        if stoch_k <= stoch_d:
            return "skip"
    
    if prediction == "short":
        # Require bearish crossover: stoch_k must be below stoch_d
        if stoch_k >= stoch_d:
            return "skip"
    
    return prediction