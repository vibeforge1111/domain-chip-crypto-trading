def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 85 and stoch_d > 80:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 15 and stoch_d < 20:
            return "skip"
    
    return prediction