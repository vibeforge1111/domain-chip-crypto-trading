def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # Require bullish alignment (k above d) and not overbought
        if stoch_k <= stoch_d or stoch_k > 80:
            return "skip"
    
    elif prediction == "short":
        # Require bearish alignment (k below d) and not oversold
        if stoch_k >= stoch_d or stoch_d < 20:
            return "skip"
    
    return prediction