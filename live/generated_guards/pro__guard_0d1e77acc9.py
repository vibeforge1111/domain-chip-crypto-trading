def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Skip if stochastic not aligned for longs (k below d)
        if stoch_k < stoch_d:
            return 'skip'
        # Skip if already overbought (reversal risk)
        if stoch_k > 85 or stoch_d > 85:
            return 'skip'
    elif prediction == 'short':
        # Skip if stochastic not aligned for shorts (k above d)
        if stoch_k > stoch_d:
            return 'skip'
        # Skip if already oversold (reversal risk)
        if stoch_k < 15 or stoch_d < 15:
            return 'skip'
    
    return prediction