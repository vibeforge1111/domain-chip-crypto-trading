def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For long signals, require bullish crossover (stoch_k > stoch_d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # For short signals, require bearish crossover (stoch_k < stoch_d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction