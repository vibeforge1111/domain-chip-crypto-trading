def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        if stoch_k <= stoch_d or stoch_k > 80:
            return 'skip'
        if vwap_dev < -0.005:
            return 'skip'
    elif prediction == 'short':
        if stoch_k >= stoch_d or stoch_k < 20:
            return 'skip'
        if vwap_dev > 0.005:
            return 'skip'
    
    if prediction == 'long' and rsi_2h > 70:
        return 'skip'
    if prediction == 'short' and rsi_2h < 30:
        return 'skip'
    
    return prediction