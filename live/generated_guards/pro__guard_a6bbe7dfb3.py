def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard with trend confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if prediction == 'long':
        if stoch_k >= stoch_d:
            return 'skip'
        if rsi_2h < 40 or bb_pct_b < 0.15:
            return 'skip'
    elif prediction == 'short':
        if stoch_k <= stoch_d:
            return 'skip'
        if rsi_2h > 60 or bb_pct_b > 0.85:
            return 'skip'
    
    return prediction