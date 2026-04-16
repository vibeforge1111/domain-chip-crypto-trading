def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_14 = features.get('rsi_14', 50)
    
    # Stochastic crossover strength
    stoch_diff = stoch_k - stoch_d
    
    # For longs: require bullish crossover (stoch_k > stoch_d) with momentum
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return "skip"
        if abs(stoch_diff) < 3:
            return "skip"
        if rsi_14 < 40:
            return "skip"
    
    # For shorts: require bearish crossover (stoch_k < stoch_d) with momentum
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return "skip"
        if abs(stoch_diff) < 3:
            return "skip"
        if rsi_14 > 60:
            return "skip"
    
    return prediction