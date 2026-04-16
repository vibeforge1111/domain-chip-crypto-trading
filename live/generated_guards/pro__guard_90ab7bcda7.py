def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Require stoch_k/stoch_d crossover alignment with prediction
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
    
    # Skip extreme stochastic levels (avoid overbought/oversold traps)
    if stoch_k < 20 or stoch_k > 80:
        return 'skip'
    
    # Confirm trend with 2h RSI
    if prediction == 'long' and rsi_2h < 45:
        return 'skip'
    if prediction == 'short' and rsi_2h > 55:
        return 'skip'
    
    # Reject trades too far from VWAP
    if abs(vwap_dev) > 0.005:
        return 'skip'
    
    return prediction