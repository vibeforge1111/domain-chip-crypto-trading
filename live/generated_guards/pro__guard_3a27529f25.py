def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Require bullish crossover for longs (stoch_k above stoch_d)
    if prediction == "long" and stoch_k <= stoch_d:
        return "skip"
    
    # Require bearish crossover for shorts (stoch_k below stoch_d)
    if prediction == "short" and stoch_k >= stoch_d:
        return "skip"
    
    # Avoid extreme overbought/oversold zones
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction