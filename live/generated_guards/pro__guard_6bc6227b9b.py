def guard(features: dict, prediction: str) -> str:
    """Filter trades using stoch_k/stoch_d crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require stochastic alignment with prediction direction
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return "skip"
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return "skip"
    
    return prediction