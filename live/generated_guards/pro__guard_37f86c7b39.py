def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    volume_ratio = features.get('volume_ratio', 1.0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if vwap_deviation < -0.005:
            return 'skip'
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if vwap_deviation > 0.005:
            return 'skip'
    
    if volume_ratio < 0.8:
        return 'skip'
    
    return prediction