def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # K must cross above D and ideally in oversold territory
        if stoch_k <= stoch_d or stoch_k < 30:
            return 'skip'
        # VWAP confirmation: price should be above VWAP
        if features.get('vwap_deviation', 0) < 0:
            return 'skip'
    elif prediction == 'short':
        # K must cross below D and ideally in overbought territory
        if stoch_k >= stoch_d or stoch_k > 70:
            return 'skip'
        # VWAP confirmation: price should be below VWAP
        if features.get('vwap_deviation', 0) > 0:
            return 'skip'
    
    return prediction