def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover timing for entry precision."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_spread = stoch_k - stoch_d
    
    if prediction == "long":
        # Require bullish crossover: stoch_k above stoch_d in oversold zone
        if stoch_spread <= 0 or stoch_d >= 25:
            return "skip"
    elif prediction == "short":
        # Require bearish crossover: stoch_k below stoch_d in overbought zone
        if stoch_spread >= 0 or stoch_d <= 75:
            return "skip"
    
    return prediction