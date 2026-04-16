def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - rejects trades when momentum misaligns."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Long: require bullish crossover or close to it
    if prediction == "long" and stoch_k < stoch_d - 10:
        return "skip"
    
    # Short: require bearish crossover or close to it
    if prediction == "short" and stoch_k > stoch_d + 10:
        return "skip"
    
    return prediction