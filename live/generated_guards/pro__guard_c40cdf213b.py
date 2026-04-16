def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # For longs: require bullish crossover (k above d) with room to run
    if prediction == "long":
        if stoch_k < stoch_d or stoch_k > 85 or stoch_d > 75:
            return "skip"
    
    # For shorts: require bearish crossover (k below d) with room to fall
    if prediction == "short":
        if stoch_k > stoch_d or stoch_k < 15 or stoch_d < 25:
            return "skip"
    
    return prediction