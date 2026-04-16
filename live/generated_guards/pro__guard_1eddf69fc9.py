def guard(features: dict, prediction: str) -> str:
    """Filter trades using stoch_k vs stoch_d crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Longs require bullish crossover (stoch_k above stoch_d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Shorts require bearish crossover (stoch_k below stoch_d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction