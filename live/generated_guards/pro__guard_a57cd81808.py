def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing filter."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Longs need bullish crossover (k above d), shorts need bearish (k below d)
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    return prediction