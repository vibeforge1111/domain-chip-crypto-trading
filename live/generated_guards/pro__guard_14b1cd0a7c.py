def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover alignment."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For longs, require bullish crossover (k crosses above d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # For shorts, require bearish crossover (k crosses below d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction