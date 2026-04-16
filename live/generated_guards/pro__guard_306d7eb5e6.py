def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Require bullish crossover (k crosses above d) and not overbought
        if stoch_k <= stoch_d or stoch_k > 80:
            return 'skip'
    
    if prediction == 'short':
        # Require bearish crossover (k crosses below d) and not oversold
        if stoch_k >= stoch_d or stoch_k < 20:
            return 'skip'
    
    return prediction