def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover for precise entry timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Require bullish crossover and momentum in oversold territory
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_k < 20:
            return 'skip'
        if 20 <= stoch_k <= 50:
            return 'skip'
    elif prediction == 'short':
        # Require bearish crossover and momentum in overbought territory
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_k > 80:
            return 'skip'
        if 50 <= stoch_k <= 80:
            return 'skip'
    
    return prediction