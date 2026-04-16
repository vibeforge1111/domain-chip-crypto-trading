def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Detect crossover: small spread between k and d (recent crossover)
    spread = abs(stoch_k - stoch_d)
    
    if prediction == 'long':
        # Stochastic crossover from oversold with tight spread
        if stoch_k < 30 or stoch_d < 30:
            if stoch_k > stoch_d and spread < 12:
                if vwap_dev > -0.003:  # Not too far below VWAP
                    return prediction
        return 'skip'
    
    if prediction == 'short':
        # Stochastic crossover from overbought with tight spread
        if stoch_k > 70 or stoch_d > 70:
            if stoch_k < stoch_d and spread < 12:
                if vwap_dev < 0.003:  # Not too far above VWAP
                    return prediction
        return 'skip'
    
    return prediction