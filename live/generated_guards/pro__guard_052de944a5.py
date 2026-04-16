def guard(features: dict, prediction: str) -> str:
    """Filter trades not aligned with stochastic crossover momentum."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject longs when stoch_k below stoch_d (bearish alignment)
    if prediction == "long" and stoch_k < stoch_d:
        return "skip"
    # Reject shorts when stoch_k above stoch_d (bullish alignment)
    if prediction == "short" and stoch_k > stoch_d:
        return "skip"
    
    return prediction