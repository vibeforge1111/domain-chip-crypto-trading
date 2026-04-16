def guard(features: dict, prediction: str) -> str:
    """Guard using stoch_k/d crossover timing with momentum confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        # Bullish crossover: fast k above slow d
        if stoch_k < stoch_d:
            return 'skip'
        # Require positive momentum
        if macd_histogram < 0:
            return 'skip'
        # Require price above VWAP
        if vwap_deviation < 0:
            return 'skip'
    elif prediction == 'short':
        # Bearish crossover: fast k below slow d
        if stoch_k > stoch_d:
            return 'skip'
        # Require negative momentum
        if macd_histogram > 0:
            return 'skip'
        # Require price below VWAP
        if vwap_deviation > 0:
            return 'skip'
    
    return prediction