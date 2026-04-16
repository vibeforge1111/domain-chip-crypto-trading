def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # For long entries, stoch_k should be above stoch_d (bullish crossover)
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        # Reject if already overbought
        if stoch_k > 80:
            return "skip"
    
    # For short entries, stoch_k should be below stoch_d (bearish crossover)
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        # Reject if already oversold
        if stoch_k < 20:
            return "skip"
    
    return prediction