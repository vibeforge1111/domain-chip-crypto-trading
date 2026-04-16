def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover alignment guard for entry timing."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Longs need stoch_k above stoch_d (bullish alignment)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Shorts need stoch_k below stoch_d (bearish alignment)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction