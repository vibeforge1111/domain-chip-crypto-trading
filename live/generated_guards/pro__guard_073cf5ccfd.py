def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require proper crossover alignment for entries
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    # Only enter in favorable stochastic zones
    if prediction == 'long' and stoch_k > 40:
        return 'skip'
    if prediction == 'short' and stoch_k < 60:
        return 'skip'
    
    return prediction