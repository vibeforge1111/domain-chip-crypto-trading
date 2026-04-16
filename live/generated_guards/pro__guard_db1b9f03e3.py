def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with regime awareness."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Require bullish crossover: stoch_k above stoch_d
        if stoch_k <= stoch_d:
            return 'skip'
        # Avoid entering when already overbought (limit at 80)
        if stoch_k > 80:
            return 'skip'
        # Ensure not starting from extreme oversold (validates fresh crossover)
        if stoch_d > 75:
            return 'skip'
    
    if prediction == 'short':
        # Require bearish crossover: stoch_k below stoch_d
        if stoch_k >= stoch_d:
            return 'skip'
        # Avoid entering when already oversold (limit at 20)
        if stoch_k < 20:
            return 'skip'
        # Ensure not starting from extreme oversold territory
        if stoch_d < 25:
            return 'skip'
    
    return prediction