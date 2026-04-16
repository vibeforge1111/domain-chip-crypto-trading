def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Longs require bullish crossover: stoch_k > stoch_d in oversold territory
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_d > 25:  # Still too high, no pullback confirmation
            return "skip"
    
    # Shorts require bearish crossover: stoch_k < stoch_d in overbought territory
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_d < 75:  # Still too low, no pullback confirmation
            return "skip"
    
    return prediction