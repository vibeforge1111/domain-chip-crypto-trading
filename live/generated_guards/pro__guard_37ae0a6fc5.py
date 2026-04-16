def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Crossover requires k above d, both in oversold, confirming momentum shift
        if not (stoch_k > stoch_d and stoch_d < 25 and stoch_k < 50):
            return "skip"
    elif prediction == "short":
        # Crossover requires k below d, both in overbought, confirming bearish shift
        if not (stoch_k < stoch_d and stoch_d > 75 and stoch_k > 50):
            return "skip"
    
    return prediction