def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing with momentum confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        # Require bullish stochastic crossover in oversold territory
        if not (stoch_k > stoch_d and stoch_d < 25):
            return 'skip'
        # Avoid longs when price is too far below VWAP (weakness)
        if vwap_dev < -0.01:
            return 'skip'
    
    elif prediction == 'short':
        # Require bearish stochastic crossover in overbought territory
        if not (stoch_k < stoch_d and stoch_d > 75):
            return 'skip'
        # Avoid shorts when price is too far above VWAP (strength)
        if vwap_dev > 0.01:
            return 'skip'
    
    return prediction