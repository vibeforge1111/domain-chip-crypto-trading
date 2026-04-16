def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing in oversold/overbought zones."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    
    if prediction == "skip":
        return prediction
    
    # Stochastic crossover with momentum confirmation
    if prediction == "long":
        # Bullish crossover in oversold territory
        if stoch_k < 25 and stoch_d < 25 and stoch_diff > 8:
            return prediction
        return "skip"
    
    if prediction == "short":
        # Bearish crossover in overbought territory
        if stoch_k > 75 and stoch_d > 75 and stoch_diff < -8:
            return prediction
        return "skip"
    
    return prediction