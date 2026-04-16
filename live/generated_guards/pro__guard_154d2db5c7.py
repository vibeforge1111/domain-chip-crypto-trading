def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Require stochastic crossover for timing precision
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_k > 80:
            return 'skip'
        if rsi_2h < 40:
            return 'skip'
    
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_k < 20:
            return 'skip'
        if rsi_2h > 60:
            return 'skip'
    
    return prediction