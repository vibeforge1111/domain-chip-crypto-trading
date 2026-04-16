def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    crossover_gap = stoch_k - stoch_d
    
    if prediction == 'long':
        # Require bullish crossover: k above d with meaningful gap
        if crossover_gap <= 0:
            return 'skip'
        # Require both in oversold territory for better timing
        if stoch_d > 30:
            return 'skip'
    elif prediction == 'short':
        # Require bearish crossover: k below d with meaningful gap
        if crossover_gap >= 0:
            return 'skip'
        # Require both in overbought territory for better timing
        if stoch_d < 70:
            return 'skip'
    
    return prediction