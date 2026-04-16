def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover alignment for entry timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # For long entries, require stoch_k > stoch_d (bullish crossover alignment)
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    
    # For short entries, require stoch_k < stoch_d (bearish crossover alignment)
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    return prediction