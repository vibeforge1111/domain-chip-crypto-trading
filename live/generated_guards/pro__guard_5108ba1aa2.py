def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For long entries, require bullish alignment (k above d) and not overbought
    if prediction == "long" and (stoch_k <= stoch_d or stoch_k > 80):
        return "skip"
    
    # For short entries, require bearish alignment (k below d) and not oversold
    if prediction == "short" and (stoch_k >= stoch_d or stoch_k < 20):
        return "skip"
    
    return prediction