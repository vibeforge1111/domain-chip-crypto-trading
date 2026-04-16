def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Long: reject if %K below %D (bearish alignment)
    if prediction == 'long' and stoch_k < stoch_d:
        return 'skip'
    
    # Short: reject if %K above %D (bullish alignment)
    if prediction == 'short' and stoch_k > stoch_d:
        return 'skip'
    
    return prediction