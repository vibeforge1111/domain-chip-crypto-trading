def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_k > 80:
            return 'skip'
    
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_k < 20:
            return 'skip'
    
    return prediction