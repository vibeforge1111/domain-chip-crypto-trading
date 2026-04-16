def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover zone detection."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Require fresh crossover zone: stoch_k within 5 points of stoch_d
    if abs(stoch_k - stoch_d) > 5:
        return "skip"
    
    # For longs: stoch_k should be below or equal to stoch_d (bullish crossover zone)
    if prediction == "long" and stoch_k > stoch_d:
        return "skip"
    
    # For shorts: stoch_k should be above or equal to stoch_d (bearish crossover zone)
    if prediction == "short" and stoch_k < stoch_d:
        return "skip"
    
    return prediction