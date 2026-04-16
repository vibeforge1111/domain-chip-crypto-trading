def guard(features: dict, prediction: str) -> str:
    """Custom guard function using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # For long entries, require bullish alignment (stoch_k > stoch_d) and not in overbought zone
    if prediction == "long":
        if stoch_k <= stoch_d or stoch_k > 80:
            return "skip"
    
    # For short entries, require bearish alignment (stoch_k < stoch_d) and not in oversold zone
    if prediction == "short":
        if stoch_k >= stoch_d or stoch_k < 20:
            return "skip"
    
    return prediction