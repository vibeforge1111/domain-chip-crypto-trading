def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Stochastic crossover: k crosses above d for longs, below for shorts
    k_crossed_above = stoch_k > stoch_d and stoch_d < 30
    k_crossed_below = stoch_k < stoch_d and stoch_d > 70
    
    if prediction == "long":
        if not k_crossed_above:
            return "skip"
        if bb_pct_b > 0.7:
            return "skip"
    elif prediction == "short":
        if not k_crossed_below:
            return "skip"
        if bb_pct_b < 0.3:
            return "skip"
    
    return prediction