def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover to time entries precisely."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Reject long if stoch_k already above stoch_d (upside momentum may be exhausted)
        if stoch_k > stoch_d:
            return 'skip'
    
    if prediction == 'short':
        # Reject short if stoch_k already below stoch_d (downside momentum may be exhausted)
        if stoch_k < stoch_d:
            return 'skip'
    
    return prediction