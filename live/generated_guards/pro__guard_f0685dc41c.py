def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    if prediction == 'long':
        # Reject if no bullish stochastic crossover
        if stoch_k <= stoch_d:
            return 'skip'
        # Reject if stoch in overbought zone (too late for longs)
        if stoch_k > 65 and stoch_d > 60:
            return 'skip'
        # Reject if 2h RSI too extended
        if rsi_2h > 68:
            return 'skip'
    
    if prediction == 'short':
        # Reject if no bearish stochastic crossover
        if stoch_k >= stoch_d:
            return 'skip'
        # Reject if stoch in oversold zone (too late for shorts)
        if stoch_k < 35 and stoch_d < 40:
            return 'skip'
        # Reject if 2h RSI too low
        if rsi_2h < 32:
            return 'skip'
    
    return prediction