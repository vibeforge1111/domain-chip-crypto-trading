def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard using stoch_k vs stoch_d."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_d > 30:
            return 'skip'
        if vwap_dev < -0.005:
            return 'skip'
    
    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_d < 70:
            return 'skip'
        if vwap_dev > 0.005:
            return 'skip'
    
    return prediction