def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing filter."""
    k = features.get("stoch_k", 50)
    d = features.get("stoch_d", 50)
    
    # For longs: require bullish alignment (k > d) and avoid overbought
    if prediction == "long":
        if k <= d:
            return "skip"
        if k > 80:
            return "skip"
    
    # For shorts: require bearish alignment (k < d) and avoid oversold
    if prediction == "short":
        if k >= d:
            return "skip"
        if k < 20:
            return "skip"
    
    return prediction