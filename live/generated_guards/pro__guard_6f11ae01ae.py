def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Require bullish crossover (k above d) in oversold zone
        if stoch_k <= stoch_d or stoch_k > 25:
            return 'skip'
    elif prediction == 'short':
        # Require bearish crossover (k below d) in overbought zone
        if stoch_k >= stoch_d or stoch_k < 75:
            return 'skip'
    
    return prediction