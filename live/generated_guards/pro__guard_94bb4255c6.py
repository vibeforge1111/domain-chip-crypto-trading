def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Stochastic crossover timing filter
    # For longs: bullish crossover (stoch_k > stoch_d) in oversold zone
    if prediction == "long":
        if stoch_k <= stoch_d or stoch_k > 40:
            return "skip"
    
    # For shorts: bearish crossover (stoch_k < stoch_d) in overbought zone
    elif prediction == "short":
        if stoch_k >= stoch_d or stoch_k < 60:
            return "skip"
    
    return prediction