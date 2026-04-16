def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Require bullish crossover: fast line above slow line
        if stoch_k <= stoch_d:
            return 'skip'
    elif prediction == 'short':
        # Require bearish crossover: fast line below slow line
        if stoch_k >= stoch_d:
            return 'skip'
    
    return prediction