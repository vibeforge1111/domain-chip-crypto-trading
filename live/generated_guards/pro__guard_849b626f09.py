def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Reject longs if stoch_k not above stoch_d (bullish crossover required)
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    # Reject shorts if stoch_k not below stoch_d (bearish crossover required)
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    # Reject longs in overbought territory
    if prediction == 'long' and stoch_k > 80:
        return 'skip'
    # Reject shorts in oversold territory
    if prediction == 'short' and stoch_k < 20:
        return 'skip'
    return prediction