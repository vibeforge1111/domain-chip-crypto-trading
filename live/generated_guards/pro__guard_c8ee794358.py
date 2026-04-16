def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Check for stochastic crossover alignment
    if prediction == 'long':
        # Bullish crossover required: stoch_k must be above stoch_d
        if stoch_k <= stoch_d:
            return 'skip'
        # Price should be above or near VWAP for longs
        if vwap_dev < -0.005:
            return 'skip'
    elif prediction == 'short':
        # Bearish crossover required: stoch_k must be below stoch_d
        if stoch_k >= stoch_d:
            return 'skip'
        # Price should be below or near VWAP for shorts
        if vwap_dev > 0.005:
            return 'skip'
    
    return prediction