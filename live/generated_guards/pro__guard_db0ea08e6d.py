def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic oscillator crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Bullish crossover timing: stoch_k above stoch_d from oversold
        if stoch_k <= stoch_d or stoch_d >= 30:
            return "skip"
    
    elif prediction == "short":
        # Bearish crossover timing: stoch_k below stoch_d from overbought
        if stoch_k >= stoch_d or stoch_d <= 70:
            return "skip"
    
    return prediction