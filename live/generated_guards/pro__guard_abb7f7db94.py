def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require stoch_k > stoch_d for longs (bullish crossover)
    if prediction == 'long' and stoch_k <= stoch_d:
        return "skip"
    
    # Require stoch_k < stoch_d for shorts (bearish crossover)
    if prediction == 'short' and stoch_k >= stoch_d:
        return "skip"
    
    return prediction