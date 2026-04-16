def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Long entries: require bullish crossover (stoch_k > stoch_d) with room to run
    if prediction == "long":
        if stoch_k <= stoch_d or stoch_k > 70:
            return "skip"
    
    # Short entries: require bearish crossover (stoch_k < stoch_d) with room to run
    if prediction == "short":
        if stoch_k >= stoch_d or stoch_k < 30:
            return "skip"
    
    return prediction