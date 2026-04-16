def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Require bullish crossover in oversold territory
        if not (stoch_k > stoch_d and stoch_k < 30):
            return "skip"
    
    elif prediction == "short":
        # Require bearish crossover in overbought territory
        if not (stoch_k < stoch_d and stoch_k > 70):
            return "skip"
    
    return prediction