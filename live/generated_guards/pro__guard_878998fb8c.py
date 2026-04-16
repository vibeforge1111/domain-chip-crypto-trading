def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require stoch_k >= stoch_d for longs (bullish alignment)
    if prediction == 'long' and stoch_k < stoch_d:
        return 'skip'
    
    # Require stoch_k <= stoch_d for shorts (bearish alignment)
    if prediction == 'short' and stoch_k > stoch_d:
        return 'skip'
    
    return prediction