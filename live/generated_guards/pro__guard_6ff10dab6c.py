def guard(features: dict, prediction: str) -> str:
    # Align with broader 2h trend using rsi_2h
    rsi_2h = features.get('rsi_2h', 50)
    if prediction == 'long' and rsi_2h < 40:
        return 'skip'
    if prediction == 'short' and rsi_2h > 60:
        return 'skip'
    
    # Avoid extreme stochastic readings
    stoch_k = features.get('stoch_k', 50)
    if prediction == 'long' and stoch_k > 85:
        return 'skip'
    if prediction == 'short' and stoch_k < 15:
        return 'skip'
    
    return prediction