def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject long if stochastic not bullish (k below d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Reject short if stochastic not bearish (k above d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction