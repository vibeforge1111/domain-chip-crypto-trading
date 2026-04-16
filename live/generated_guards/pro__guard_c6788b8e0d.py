def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing filter for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        if not (stoch_k > stoch_d and stoch_k < 30):
            return "skip"
    elif prediction == "short":
        if not (stoch_k < stoch_d and stoch_k > 70):
            return "skip"
    
    return prediction