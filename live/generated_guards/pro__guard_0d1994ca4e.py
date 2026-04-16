def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover quality."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    stoch_diff = abs(stoch_k - stoch_d)
    
    # Reject when k and d are too close (unclear crossover, choppy)
    if stoch_diff < 2:
        return "skip"
    
    # Reject when both in middle zone with weak separation
    if 20 < stoch_k < 80 and 20 < stoch_d < 80 and stoch_diff < 4:
        return "skip"
    
    return prediction