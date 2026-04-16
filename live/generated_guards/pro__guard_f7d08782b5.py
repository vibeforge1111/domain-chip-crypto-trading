def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Long: requires bullish crossover (k crosses above d) and not overbought
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 75:
            return "skip"
    
    # Short: requires bearish crossover (k crosses below d) and not oversold
    if prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 25:
            return "skip"
    
    return prediction