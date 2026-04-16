def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    sk = features.get('stoch_k', 50)
    sd = features.get('stoch_d', 50)
    
    if prediction == 'long' and sk <= sd:
        return 'skip'
    if prediction == 'short' and sk >= sd:
        return 'skip'
    
    return prediction