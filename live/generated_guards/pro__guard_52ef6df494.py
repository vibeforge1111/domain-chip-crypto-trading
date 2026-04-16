def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Reject if no bullish crossover (k below or equal d)
        if stoch_k <= stoch_d:
            return 'skip'
        # Reject if already overbought
        if stoch_k > 85:
            return 'skip'
    
    if prediction == 'short':
        # Reject if no bearish crossover (k above or equal d)
        if stoch_k >= stoch_d:
            return 'skip'
        # Reject if already oversold
        if stoch_k < 15:
            return 'skip'
    
    return prediction