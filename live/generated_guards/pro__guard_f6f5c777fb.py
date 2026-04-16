def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with momentum confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        # Skip if no bullish crossover or price not above VWAP
        if stoch_k <= stoch_d or vwap_dev < 0:
            return 'skip'
    elif prediction == 'short':
        # Skip if no bearish crossover or price not below VWAP
        if stoch_k >= stoch_d or vwap_dev > 0:
            return 'skip'
    return prediction