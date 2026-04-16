def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_14 = features.get('rsi_14', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == 'skip':
        return prediction
    
    # Check for valid stochastic crossover with momentum
    if stoch_k > stoch_d:
        # Bullish crossover - for longs
        if stoch_k - stoch_d < 3:
            return 'skip'
        if stoch_d > 30 or rsi_14 > 60 or vwap_dev > 0.002:
            return 'skip'
    else:
        # Bearish crossover - for shorts
        if stoch_d - stoch_k < 3:
            return 'skip'
        if stoch_d < 70 or rsi_14 < 40 or vwap_dev < -0.002:
            return 'skip'
    
    return prediction