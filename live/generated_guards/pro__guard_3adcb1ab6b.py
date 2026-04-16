def guard(features: dict, prediction: str) -> str:
    """Mean-reversion timing guard: skip entries at RSI extremes ripe for reversal."""
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long':
        # Skip long when overbought: RSI extreme or both 15m and 2h elevated
        if rsi_14 > 72 or (rsi_14 > 62 and rsi_2h > 58):
            return 'skip'
        # Stochastic confirms momentum exhaustion
        if stoch_k > 85:
            return 'skip'
    
    elif prediction == 'short':
        # Skip short when oversold: RSI extreme or both 15m and 2h suppressed
        if rsi_14 < 28 or (rsi_14 < 38 and rsi_2h < 42):
            return 'skip'
        # Stochastic confirms momentum exhaustion
        if stoch_k < 15:
            return 'skip'
    
    return prediction