def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Reject if not in bullish alignment or already overbought
        if stoch_k <= stoch_d or stoch_k > 75:
            return 'skip'
    
    if prediction == 'short':
        # Reject if not in bearish alignment or already oversold
        if stoch_k >= stoch_d or stoch_k < 25:
            return 'skip'
    
    return prediction