def guard(features: dict, prediction: str) -> str:
    """Filter trades based on Stochastic crossover alignment."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For long: k should be above d (bullish alignment)
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 80 or stoch_k < 25:
            return "skip"
    
    # For short: k should be below d (bearish alignment)
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 20 or stoch_k > 75:
            return "skip"
    
    return prediction