def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters entries not at proper stoch extremes."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Bullish crossover setup: both oversold and k already above d
        if stoch_k < 30 and stoch_d < 30 and stoch_k > stoch_d:
            return prediction
        return 'skip'
    
    if prediction == 'short':
        # Bearish crossover setup: both overbought and k already below d
        if stoch_k > 70 and stoch_d > 70 and stoch_k < stoch_d:
            return prediction
        return 'skip'
    
    return prediction