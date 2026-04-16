def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using stochastic crossover."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_cross = stoch_k - stoch_d
    
    # Reject longs if stoch_k below stoch_d (bearish crossover)
    if prediction == "long" and stoch_k < stoch_d:
        return "skip"
    
    # Reject shorts if stoch_k above stoch_d (bullish crossover)
    if prediction == "short" and stoch_k > stoch_d:
        return "skip"
    
    # Additional quality filter: require meaningful crossover separation
    if abs(stoch_cross) < 3:
        return "skip"
    
    return prediction