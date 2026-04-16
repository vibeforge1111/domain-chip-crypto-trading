def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Stochastic crossover timing: stoch_k > stoch_d = bullish, < = bearish
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_k > 80 or rsi_2h > 70:  # Avoid overbought entries
            return 'skip'
        if vwap_dev < -0.01:  # Skip if well below VWAP
            return 'skip'
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_k < 20 or rsi_2h < 30:  # Avoid oversold entries
            return 'skip'
        if vwap_dev > 0.01:  # Skip if well above VWAP
            return 'skip'
    
    return prediction