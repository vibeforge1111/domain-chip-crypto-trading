def guard(features: dict, prediction: str) -> str:
    """Guard using stoch_k/d crossover for precise entry timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    stoch_diff = stoch_k - stoch_d
    
    # Require meaningful crossover strength
    if abs(stoch_diff) < 5:
        return 'skip'
    
    # For long entries: stoch_k must be above stoch_d (bullish crossover)
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        # Avoid entering when overbought (potential reversal)
        if stoch_k > 75:
            return 'skip'
    
    # For short entries: stoch_k must be below stoch_d (bearish crossover)
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        # Avoid entering when oversold (potential bounce)
        if stoch_k < 25:
            return 'skip'
    
    return prediction