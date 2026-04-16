def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Reject longs if bearish crossover (stoch_k below stoch_d)
    if prediction == 'long' and stoch_k < stoch_d:
        return 'skip'
    
    # Reject shorts if bullish crossover (stoch_k above stoch_d)
    if prediction == 'short' and stoch_k > stoch_d:
        return 'skip'
    
    return prediction