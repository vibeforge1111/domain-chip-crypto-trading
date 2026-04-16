def guard(features: dict, prediction: str) -> str:
    """Filter trades using Stochastic crossover with overbought/oversold confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Stochastic bullish crossover: k above d in oversold zone
        if stoch_k <= stoch_d or stoch_d > 30:
            return 'skip'
    elif prediction == 'short':
        # Stochastic bearish crossover: k below d in overbought zone
        if stoch_k >= stoch_d or stoch_d < 70:
            return 'skip'
    
    return prediction