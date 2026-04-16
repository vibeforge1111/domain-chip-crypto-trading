def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require bullish crossover (k above d) for longs
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        # Reject if not in oversold territory (avoid chasing extended moves)
        if stoch_k > 30:
            return 'skip'
    
    # Require bearish crossover (k below d) for shorts
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        # Reject if not in overbought territory
        if stoch_k < 70:
            return 'skip'
    
    return prediction