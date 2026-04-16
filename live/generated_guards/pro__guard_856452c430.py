def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Stochastic crossover timing: longs need stoch_k >= stoch_d, shorts need stoch_k <= stoch_d
    if prediction == 'long' and stoch_k < stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k > stoch_d:
        return 'skip'
    
    # Additional filter: reject if stochastic crossover occurs against the 2h trend
    if prediction == 'long' and rsi_2h < 45 and stoch_k < stoch_d:
        return 'skip'
    if prediction == 'short' and rsi_2h > 55 and stoch_k > stoch_d:
        return 'skip'
    
    return prediction