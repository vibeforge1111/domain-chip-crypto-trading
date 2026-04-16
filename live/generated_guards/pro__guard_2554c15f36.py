def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require clear crossover signal
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Skip if stochastic in extreme zone (reversal risk)
    if stoch_k > 80 or stoch_k < 20:
        return "skip"
    
    return prediction