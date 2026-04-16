def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing in extreme zones."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Reject if no bullish crossover or not in oversold territory
        if not (stoch_k > stoch_d and stoch_d < 25):
            return "skip"
    elif prediction == "short":
        # Reject if no bearish crossover or not in overbought territory
        if not (stoch_k < stoch_d and stoch_d > 75):
            return "skip"
    
    return prediction