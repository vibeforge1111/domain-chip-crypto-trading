def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    stoch_diff = stoch_k - stoch_d
    
    # Require bullish crossover for longs, bearish for shorts
    if prediction == "long" and stoch_diff <= 0:
        return "skip"
    if prediction == "short" and stoch_diff >= 0:
        return "skip"
    
    return prediction