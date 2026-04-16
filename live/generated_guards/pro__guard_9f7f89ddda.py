def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing precision."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Validate bounds
    if not (0 <= stoch_k <= 100 and 0 <= stoch_d <= 100):
        return prediction
    
    # For long: stoch_k must be below stoch_d (bullish crossover incoming)
    if prediction == "long":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k > 30:  # Not in oversold territory yet
            return "skip"
    
    # For short: stoch_k must be above stoch_d (bearish crossover incoming)
    if prediction == "short":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k < 70:  # Not in overbought territory yet
            return "skip"
    
    return prediction