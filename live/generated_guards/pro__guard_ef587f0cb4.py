def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing and zone."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == "long":
        # Reject if stoch_k already above stoch_d (missed crossover timing)
        if stoch_k > stoch_d:
            return "skip"
        # Reject if already in oversold (risky reversal zone)
        if stoch_k < 20:
            return "skip"
    elif prediction == "short":
        # Reject if stoch_k already below stoch_d (missed crossover timing)
        if stoch_k < stoch_d:
            return "skip"
        # Reject if already in overbought (risky reversal zone)
        if stoch_k > 80:
            return "skip"
    return prediction