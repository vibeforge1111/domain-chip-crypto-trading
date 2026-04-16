def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard with RSI context filter."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 30:
            return "skip"
        if rsi_2h > 65:
            return "skip"
    
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 70:
            return "skip"
        if rsi_2h < 35:
            return "skip"
    
    return prediction