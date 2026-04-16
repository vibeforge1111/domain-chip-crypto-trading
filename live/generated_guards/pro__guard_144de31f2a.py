def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Reject long if stochastic shows bearish alignment (k below d)
        if stoch_k < stoch_d:
            return "skip"
        # Reject long if overbought (high chance of reversal)
        if stoch_k > 80:
            return "skip"
    elif prediction == "short":
        # Reject short if stochastic shows bullish alignment (k above d)
        if stoch_k > stoch_d:
            return "skip"
        # Reject short if oversold (high chance of bounce)
        if stoch_k < 20:
            return "skip"
    
    return prediction