def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    stoch_spread = stoch_k - stoch_d
    
    # Require meaningful stochastic crossover for entry timing
    if prediction == 'long':
        # Reject if not in bullish crossover (k above d)
        if stoch_spread <= 3:
            return "skip"
    elif prediction == 'short':
        # Reject if not in bearish crossover (k below d)
        if stoch_spread >= -3:
            return "skip"
    
    return prediction