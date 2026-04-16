def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    crossover_gap = abs(stoch_k - stoch_d)
    
    if prediction == 'long':
        # Reject if not near crossover (gap > 5) or not in oversold zone
        if crossover_gap > 5 or (stoch_k > 30 and stoch_d > 30):
            return 'skip'
    elif prediction == 'short':
        # Reject if not near crossover (gap > 5) or not in overbought zone
        if crossover_gap > 5 or (stoch_k < 70 and stoch_d < 70):
            return 'skip'
    
    return prediction