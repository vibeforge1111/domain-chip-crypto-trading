def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Require bullish crossover: k just crossed above d, or k rising from oversold
        if stoch_k <= stoch_d:
            return "skip"
        # Additional filter: not already overbought (risky to chase)
        if stoch_k > 80:
            return "skip"
    elif prediction == "short":
        # Require bearish crossover: k just crossed below d, or k falling from overbought
        if stoch_k >= stoch_d:
            return "skip"
        # Additional filter: not already oversold (risky to short)
        if stoch_k < 20:
            return "skip"
    
    return prediction