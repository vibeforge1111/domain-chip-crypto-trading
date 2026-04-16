def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover for precise entry timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # For longs: bullish crossover with stoch_d in oversold zone + price above VWAP
    if prediction == 'long':
        if stoch_k <= stoch_d:
            return 'skip'
        if stoch_d > 30:
            return 'skip'
        if vwap_deviation < 0:
            return 'skip'
        if obv_slope < 0:
            return 'skip'
    
    # For shorts: bearish crossover with stoch_d in overbought zone + price below VWAP
    if prediction == 'short':
        if stoch_k >= stoch_d:
            return 'skip'
        if stoch_d < 70:
            return 'skip'
        if vwap_deviation > 0:
            return 'skip'
        if obv_slope > 0:
            return 'skip'
    
    return prediction