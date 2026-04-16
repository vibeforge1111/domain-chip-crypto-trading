def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    spread = stoch_k - stoch_d
    
    # Require minimum spread to confirm genuine crossover momentum
    if abs(spread) < 5:
        return 'skip'
    
    # For longs: stoch_k must be above stoch_d (bullish crossover)
    if prediction == 'long' and spread <= 0:
        return 'skip'
    
    # For shorts: stoch_k must be below stoch_d (bearish crossover)
    if prediction == 'short' and spread >= 0:
        return 'skip'
    
    # Reject overbought/oversold extremes (likely reversal zones)
    if prediction == 'long' and stoch_k > 80:
        return 'skip'
    if prediction == 'short' and stoch_k < 20:
        return 'skip'
    
    return prediction