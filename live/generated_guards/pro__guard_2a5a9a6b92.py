def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Bullish crossover: k crosses above d in oversold zone (early reversal)
        if not (stoch_k > stoch_d and stoch_d < 30 and stoch_k < 50):
            return 'skip'
    
    elif prediction == 'short':
        # Bearish crossover: k crosses below d in overbought zone (early reversal)
        if not (stoch_k < stoch_d and stoch_d > 70 and stoch_k > 50):
            return 'skip'
    
    return prediction