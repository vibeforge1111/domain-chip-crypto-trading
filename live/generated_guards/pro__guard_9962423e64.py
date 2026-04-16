def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover quality."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    
    # Skip if no clear momentum divergence between k and d
    if abs(stoch_diff) < 3:
        return "skip"
    
    # For long signals, require bullish setup: k above d or k crossing up
    if prediction == "long":
        if stoch_k < stoch_d and stoch_diff > -5:
            return "skip"
    
    # For short signals, require bearish setup: k below d or k crossing down
    if prediction == "short":
        if stoch_k > stoch_d and stoch_diff < 5:
            return "skip"
    
    return prediction