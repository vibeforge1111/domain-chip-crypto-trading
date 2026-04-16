def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters entries not at fresh crossovers."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # For longs: require bullish crossover (k crosses above d)
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
    
    # For shorts: require bearish crossover (k crosses below d)
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
    
    return prediction