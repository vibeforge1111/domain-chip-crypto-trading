def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Stochastic crossover detection
    k_above_d = stoch_k > stoch_d
    k_below_d = stoch_k < stoch_d
    crossover_gap = abs(stoch_k - stoch_d)
    
    if prediction == "long":
        # Reject if not showing bullish crossover or too extended
        if not (k_above_d and stoch_k < 50 and crossover_gap > 8):
            return "skip"
    
    if prediction == "short":
        # Reject if not showing bearish crossover or too extended
        if not (k_below_d and stoch_k > 50 and crossover_gap > 8):
            return "skip"
    
    return prediction