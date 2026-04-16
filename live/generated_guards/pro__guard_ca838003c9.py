def guard(features: dict, prediction: str) -> str:
    """Custom guard function using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    
    # Reject if crossover is weak or unclear
    if abs(stoch_diff) < 3:
        return "skip"
    
    # Long requires stoch_k above stoch_d (bullish crossover)
    if prediction == "long" and stoch_diff <= 0:
        return "skip"
    
    # Short requires stoch_k below stoch_d (bearish crossover)
    if prediction == "short" and stoch_diff >= 0:
        return "skip"
    
    return prediction