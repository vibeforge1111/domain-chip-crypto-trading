def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover confirmation."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For longs: require k above d (bullish crossover)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # For shorts: require k below d (bearish crossover)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction