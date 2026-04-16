def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)

    if prediction == 'long':
        # Reject if no bullish crossover (K above D indicates momentum shift)
        if stoch_k <= stoch_d:
            return 'skip'
        # Reject if stochastic entering overbought territory
        if stoch_k > 75:
            return 'skip'
        # Confirm with VWAP alignment (price should be above VWAP)
        if vwap_dev < 0:
            return 'skip'

    if prediction == 'short':
        # Reject if no bearish crossover (K below D indicates momentum shift)
        if stoch_k >= stoch_d:
            return 'skip'
        # Reject if stochastic entering oversold territory
        if stoch_k < 25:
            return 'skip'
        # Confirm with VWAP alignment (price should be below VWAP)
        if vwap_dev > 0:
            return 'skip'

    return prediction