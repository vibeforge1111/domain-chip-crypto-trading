def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    stoch_diff = stoch_k - stoch_d
    
    if prediction == 'long':
        if stoch_diff <= 0:
            return 'skip'
        if stoch_k > 85:
            return 'skip'
    elif prediction == 'short':
        if stoch_diff >= 0:
            return 'skip'
        if stoch_k < 15:
            return 'skip'
    
    return prediction