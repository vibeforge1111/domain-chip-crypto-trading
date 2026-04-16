def guard(features: dict, prediction: str) -> str:
    """Custom guard function using stochastic crossover for entry timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Ensure crossover has sufficient separation (minimum 5 points)
    crossover_strength = abs(stoch_k - stoch_d)
    if crossover_strength < 5:
        return "skip"
    
    # For long entries, require bullish crossover (stoch_k above stoch_d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # For short entries, require bearish crossover (stoch_k below stoch_d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    return prediction