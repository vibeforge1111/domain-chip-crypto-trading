def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    stoch_diff = stoch_k - stoch_d
    
    # Reject longs when stoch_k below stoch_d (bearish crossover)
    if prediction == 'long' and stoch_diff < -5:
        return "skip"
    
    # Reject shorts when stoch_k above stoch_d (bullish crossover)
    if prediction == 'short' and stoch_diff > 5:
        return "skip"
    
    return prediction