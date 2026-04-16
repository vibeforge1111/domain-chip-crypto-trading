def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        # Bullish crossover: stoch_k must be above stoch_d
        if stoch_k <= stoch_d:
            return 'skip'
        # Must have oversold reading
        if stoch_k > 35:
            return 'skip'
        # Wider RSI context should not be bearish
        if rsi_2h < 40:
            return 'skip'
    
    if prediction == 'short':
        # Bearish crossover: stoch_k must be below stoch_d
        if stoch_k >= stoch_d:
            return 'skip'
        # Must have overbought reading
        if stoch_k < 65:
            return 'skip'
        # Wider RSI context should not be bullish
        if rsi_2h > 60:
            return 'skip'
    
    return prediction