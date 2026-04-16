def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Detect stochastic crossover momentum
    # stoch_k above stoch_d = bullish momentum, below = bearish momentum
    if stoch_k <= stoch_d:
        # Reject long entries when no bullish crossover signal
        if prediction == 'long':
            return 'skip'
    if stoch_k >= stoch_d:
        # Reject short entries when no bearish crossover signal  
        if prediction == 'short':
            return 'skip'
    
    # Filter entries at extreme overbought/oversold levels (avoid reversals)
    if prediction == 'long' and stoch_k > 80:
        return 'skip'
    if prediction == 'short' and stoch_k < 20:
        return 'skip'
    
    return prediction