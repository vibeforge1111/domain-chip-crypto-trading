def guard(features: dict, prediction: str) -> str:
    """Guard function based on stochastic crossover for entry timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if prediction == 'long':
        # Require bullish stochastic crossover + favorable price position
        if stoch_k <= stoch_d:
            return 'skip'
        if vwap_dev < -0.015:
            return 'skip'
        if bb_pct_b < 0.15:
            return 'skip'
    
    elif prediction == 'short':
        # Require bearish stochastic crossover + favorable price position
        if stoch_k >= stoch_d:
            return 'skip'
        if vwap_dev > 0.015:
            return 'skip'
        if bb_pct_b > 0.85:
            return 'skip'
    
    return prediction