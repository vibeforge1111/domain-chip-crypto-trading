def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Stochastic crossover alignment check
    if prediction == "long":
        # For longs: require bullish alignment (stoch_k >= stoch_d)
        if stoch_k < stoch_d:
            return "skip"
        # Reject longs when stochastic is deeply overbought (reversal risk)
        if stoch_k > 85:
            return "skip"
    elif prediction == "short":
        # For shorts: require bearish alignment (stoch_k <= stoch_d)
        if stoch_k > stoch_d:
            return "skip"
        # Reject shorts when stochastic is deeply oversold (reversal risk)
        if stoch_k < 15:
            return "skip"
    
    return prediction