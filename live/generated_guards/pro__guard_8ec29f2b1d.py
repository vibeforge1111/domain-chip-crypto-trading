def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Stochastic crossover timing: long requires k > d, short requires k < d
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    return prediction