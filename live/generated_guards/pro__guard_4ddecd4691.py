def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 75 or stoch_d > 75:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 25 or stoch_d < 25:
            return "skip"
    
    return prediction