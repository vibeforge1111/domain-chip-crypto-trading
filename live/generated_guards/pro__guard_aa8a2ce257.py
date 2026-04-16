def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using stochastic crossover timing."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For long entries: require stoch_k above stoch_d (bullish alignment)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # For short entries: require stoch_k below stoch_d (bearish alignment)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction