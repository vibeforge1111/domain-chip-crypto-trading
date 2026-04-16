def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Only long if stoch_k above stoch_d (bullish crossover)
        if stoch_k <= stoch_d:
            return 'skip'
    elif prediction == 'short':
        # Only short if stoch_k below stoch_d (bearish crossover)
        if stoch_k >= stoch_d:
            return 'skip'
    return prediction