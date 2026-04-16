def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if prediction == 'long':
        # Skip if higher timeframe overbought
        if rsi_2h > 70:
            return 'skip'
        # Skip if K already crossed down through D (bearish signal)
        if stoch_k < stoch_d and stoch_k > 60:
            return 'skip'
        # Skip if near upper band resistance
        if bb_pct_b > 0.9:
            return 'skip'
    
    if prediction == 'short':
        # Skip if higher timeframe oversold
        if rsi_2h < 30:
            return 'skip'
        # Skip if K already crossed up through D (bullish signal)
        if stoch_k > stoch_d and stoch_k < 40:
            return 'skip'
        # Skip if near lower band support
        if bb_pct_b < 0.1:
            return 'skip'
    
    return prediction