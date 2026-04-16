def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    diff = stoch_k - stoch_d
    
    # Stoch crossover timing guard
    # For longs: reject if stoch_k already above stoch_d in overbought (missed crossover)
    if prediction == 'long' and stoch_k > 80 and diff > 0:
        return 'skip'
    
    # For shorts: reject if stoch_k already below stoch_d in oversold (missed crossover)
    if prediction == 'short' and stoch_k < 20 and diff < 0:
        return 'skip'
    
    return prediction